import abc


class XCost(object):
  """ This abstract class declares virtual methods for computing the terminal
  cost value and its derivatives.

  The running cost depends on the state vectors, which it has n values.
  """
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def createData(self, n):
    """ Creates the terminal cost data structure.

    :param n: dimension of the state
    """
    pass

  @abc.abstractmethod
  def l(self, system, data, x):
    """ Evaluates the terminal cost function and stores the result in data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: terminal cost
    """
    pass

  @abc.abstractmethod
  def lx(self, system, data, x):
    """ Evaluates the Jacobian of the terminal cost function and stores the
    result in data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: Jacobian of the terminal cost
    """
    pass

  @abc.abstractmethod
  def lxx(self, system, data, x):
    """ Evaluates the Hessian of the terminal cost function and stores the
    result in data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: Hessian of the terminal cost
    """
    pass


class XUCost(object):
  """ This abstract class declares virtual methods for computing the running
  cost value and its derivatives.

  The running cost depends on the state and control vectors, those vectors have
  n and m dimensions, respectively.
  """
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def createData(self, n, m):
    """ Creates the terminal cost data structure

    :param n: dimension of the state
    :param m: dimensions of the control
    """
    pass

  @abc.abstractmethod
  def l(self, system, data, x, u):
    """ Evaluates the running cost function and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: running cost
    """
    pass

  @abc.abstractmethod
  def lx(self, system, data, x, u):
    """ Evaluates the Jacobian of the running cost function w.r.t. the state
    and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Jacobian of the running cost w.r.t. the state
    """
    pass

  @abc.abstractmethod
  def lu(self, system, data, x, u):
    """ Evaluates the Jacobian of the running cost function w.r.t. the control
    and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Jacobian of the residual vector w.r.t. the control
    """
    pass

  @abc.abstractmethod
  def lxx(self, system, data, x, u):
    """ Evaluates the Hessian of the running cost w.r.t. the state function and
    stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Hessian of the running cost w.r.t. the state
    """
    pass

  @abc.abstractmethod
  def luu(self, system, data, x, u):
    """ Evaluates the Hessian of the running cost function w.r.t. the control
    and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Hessian of the running cost w.r.t. the control
    """
    pass

  @abc.abstractmethod
  def lux(self, system, data, x, u):
    """ Evaluates the running cost derivatives w.r.t. the control and state and
    stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: derivatives of the running cost w.r.t. the state and control
    """
    pass


class TerminalCost(XCost):
  """ This abstract class declares virtual methods for computing the terminal
  cost value and its derivatives.

  An important remark here is that the terminal cost is computed from linear
  residual vector.
  """
  __metaclass__ = abc.ABCMeta

  def createData(self, n):
    """ Creates the terminal cost data structure.

    :param n: dimension of the state
    """
    from cddp.data import TerminalCostData
    return TerminalCostData(n)

  @abc.abstractmethod
  def xr(self, system, data, x):
    """ Evaluates the residual vector and stores the result in data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: state-residual vector
    """
    pass


class TerminalResidualCost(XCost):
  """ This abstract class declares virtual methods for computing the terminal
  cost value and its derivatives.

  An important remark here is that the terminal cost is computed from general
  residual vector r(x). Therefore, compared to the TerminalCost class, it is
  needed additionally to provide information about the residual derivatives
  w.r.t. the state rx.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, k):
    """ Constructs a terminal cost and its residual vector data.

    The residual vector dimension is defined by the user and passed it in the
    construction of this class. It generates later the appropriate data
    structure of the user-defined terminal cost function.
    :param k: residual vector dimension
    """
    # Residual vector dimension
    self.k = k

  def createData(self, n):
    """ Creates the terminal cost data structure and its residual.

    :param n: dimension of the state
    """
    from cddp.data import TerminalResidualCostData
    return TerminalResidualCostData(n, self.k)

  @abc.abstractmethod
  def r(self, system, data, x):
    """ Evaluates the residual vector and stores the result in data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: residual vector
    """
    pass

  @abc.abstractmethod
  def rx(self, system, data, x):
    """ Evaluates the Jacobian of the residual vector and stores the result in
    data.

    :param system: system
    :param data: terminal cost data
    :param x: state vector
    :returns: Jacobian of the residual vector
    """
    pass


class RunningCost(XUCost):
  """ This abstract class declares virtual methods for computing the running
  cost value and its derivatives.

  An important remark here is that the running cost is computed from linear
  residual vector on the state xr and control ur.
  """
  __metaclass__ = abc.ABCMeta

  def createData(self, n, m):
    """
    :param n: dimension of the state
    :param m: dimensions of the control
    """
    from cddp.data import RunningCostData
    return RunningCostData(n, m)

  @abc.abstractmethod
  def xr(self, system, data, x, u):
    """ Evaluates the residual state vector and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: state-residual vector
    """
    pass

  @abc.abstractmethod
  def ur(self, system, data, x, u):
    """ Evaluates the residual control vector and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: control-residual vector
    """
    pass


class RunningResidualCost(XUCost):
  """ This abstract class declares virtual methods for computing the running
  cost value and its derivatives.

  An important remark here is that the running cost is computed from general
  residual vector on the state and control, i.e. r(x,u). Therefore, compared
  to the RunningCost class, it is additionally needed to provide the information
  of the residual derivatives w.r.t. the state rx and control ru. The residual
  Hessians (rxx, ruu and rux) are neglected in Gauss-Newton steps.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, k):
    """ Constructs a terminal cost and its residual vector data.

    The residual vector dimension is defined by the user and passed it in the
    construction of this class. It generates later the appropriate data
    structure of the user-defined terminal cost function.
    :param k: residual vector dimension
    """
    # Residual vector dimension
    self.k = k

  def createData(self, n, m):
    """ Creates the data structure for the running cost and its residual.

    :param n: dimension of the state
    :param m: dimensions of the control
    """
    from cddp.data import RunningResidualCostData
    return RunningResidualCostData(n, m, self.k)

  @abc.abstractmethod
  def r(self, system, data, x, u):
    """ Evaluates the residual vector and stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: residual vector
    """
    pass

  @abc.abstractmethod
  def rx(self, system, data, x, u):
    """ Evaluates the Jacobian of the residual vector w.r.t. the state and 
    stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Jacobian of the residual vector w.r.t. the state
    """
    pass

  @abc.abstractmethod
  def ru(self, system, data, x, u):
    """ Evaluates the Jacobian of the residual vector w.r.t. the control and
    stores the result in data.

    :param system: system
    :param data: running cost data
    :param x: state vector
    :param u: control vector
    :returns: Jacobian of the residual vector w.r.t. the control
    """
    pass
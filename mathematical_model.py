from docplex.mp.model import Model


def CapTradePolicy(Vic, CE, CEr, D, Cap, PC, PCr, SP, FC, numOfFactories, Emax):
    # Create a new model
    model = Model(name='Cap&Trade')

    # Define the set of factories
    factories = range(1, numOfFactories+1)

    # Define the decision variables
    beta = model.continuous_var(name='beta', lb=0)
    Max = model.continuous_var(name='Max', lb=0)
    Q = model.continuous_var_dict(factories, name='Q')
    W = model.continuous_var_dict(factories, name='W')
    eb = model.continuous_var_dict(factories, name='eb')
    es = model.continuous_var_dict(factories, name='es')
    QW = model.continuous_var_dict(factories, name='QW')
    u1 = model.continuous_var_dict(factories, name='u1')
    u2 = model.continuous_var_dict(factories, name='u2')
    u3 = model.continuous_var_dict(factories, name='u3')
    u4 = model.continuous_var_dict(factories, name='u4')
    u5 = model.continuous_var_dict(factories, name='u5')
    u6 = model.continuous_var_dict(factories, name='u6')
    u7 = model.continuous_var_dict(factories, name='u7')
    u8 = model.continuous_var_dict(factories, name='u8')
    u9 = model.continuous_var_dict(factories, name='u9')
    u10 = model.continuous_var_dict(factories, name='u10')

    z1 = model.binary_var_dict(factories, name='z1')
    z2 = model.binary_var_dict(factories, name='z2')
    z3 = model.binary_var_dict(factories, name='z3')
    z4 = model.binary_var_dict(factories, name='z4')
    z5 = model.binary_var_dict(factories, name='z5')
    z6 = model.binary_var_dict(factories, name='z6')
    z7 = model.binary_var_dict(factories, name='z7')
    z8 = model.binary_var_dict(factories, name='z8')
    z9 = model.binary_var_dict(factories, name='z9')
    z10 = model.binary_var_dict(factories, name='z10')

    # Define the objective function
    model.minimize(model.sum(beta*Emax
                   for i in factories))

    # Define the constraints
    model.add_constraint()
    model.add_constraint()
    model.add_constraint()

    # Solve the model
    solution = model.solve()

    return solution

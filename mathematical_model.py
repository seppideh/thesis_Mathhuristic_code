from docplex.mp.model import Model


def CapTradePolicy(CE, CEr, D, Cap, PC, PCr, SP, FC, numOfFactories, Emax, H, M, gamma):
    # Create a new model
    model = Model(name='Cap&Trade')

    # Define the set of factories
    factories = range(numOfFactories)

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
    model.minimize(gamma*sum(beta*Emax
                   for i in factories)+gamma*Max
                   - sum(SP[i]*Q[i]-Q[i]*PC[i]+QW[i] *
                         (PC[i]-PCr[i])-FC[i]*W[i] for i in factories)
                   + sum(eb[i]*H for i in factories)-sum(es[i]*H for i in factories))

    model.add_constraint(beta <= 1)
    model.add_constraint(Max >= sum(
        eb[i] for i in factories)-sum(es[i] for i in factories))

    for i in factories:
        model.add_constraint(Q[i] >= D[i])
        model.add_constraint(Q[i] <= Cap[i])
        model.add_constraint(
            Q[i]*CE[i]+QW[i]*(CEr[i]-CE[i])+es[i] <= beta*Emax+eb[i])
        model.add_constraint(QW[i] <= Q[i])
        model.add_constraint(QW[i] <= Cap[i]*W[i])
        model.add_constraint(D[i]*W[i] <= QW[i])
        model.add_constraint(W[i] <= 1)
        model.add_constraint(SP[i]-PC[i] == -u1[i]+u2[i]+CE[i]*u3[i]-u4[i])
        model.add_constraint(-FC[i] == -Cap[i]*u5[i]+D[i]*u6[i]+u7[i]-u8[i])
        model.add_constraint(
            PC[i]-PCr[i] == (CEr[i]-CE[i])*u3[i]+u4[i]+u5[i]-u6[i])
        model.add_constraint(-H == -u3[i]-u9[i])
        model.add_constraint(H == u3[i]-u10[i])
        model.add_constraint(u1[i] <= M*(1-z1[i]))
        model.add_constraint(-(D[i]-Q[i]) <= M*z1[i])
        model.add_constraint(u2[i] <= M*(1-z2[i]))
        model.add_constraint(-(Q[i]-Cap[i]) <= M*z2[i])
        model.add_constraint(u3[i] <= M*(1-z3[i]))
        model.add_constraint(-(Q[i]*CE[i]+QW[i] *
                             (CEr[i]-CE[i])+es[i]-beta*Emax-eb[i]) <= M*z3[i])
        model.add_constraint(u4[i] <= M*(1-z4[i]))
        model.add_constraint(-(QW[i]-Q[i]) <= M*z4[i])
        model.add_constraint(u5[i] <= M*(1-z5[i]))
        model.add_constraint(-(QW[i]-Cap[i]*W[i]) <= M*z5[i])
        model.add_constraint(u6[i] <= M*(1-z6[i]))
        model.add_constraint(-(D[i]*W[i]-QW[i]) <= M*z6[i])
        model.add_constraint(u7[i] <= M*(1-z7[i]))
        model.add_constraint(-(W[i]-1) <= M*z7[i])
        model.add_constraint(u8[i] <= M*(1-z8[i]))
        model.add_constraint(W[i] <= M*z8[i])
        model.add_constraint(u9[i] <= M*(1-z9[i]))
        model.add_constraint(eb[i] <= M*z9[i])
        model.add_constraint(u10[i] <= M*(1-z10[i]))
        model.add_constraint(es[i] <= M*z10[i])

    # Solve the model
    solution = model.solve()

    beta = solution.get_value(beta)

    Q_values = {}
    for var_name, var in Q.items():
        Q_value = solution.get_value(var)
        Q_values[var_name] = Q_value

    W_values = {}
    for var_name, var in W.items():
        W_value = solution.get_value(var)
        W_values[var_name] = W_value
    QW_values = {}
    for var_name, var in QW.items():
        QW_value = solution.get_value(var)
        QW_values[var_name] = QW_value
    eb_values = {}
    for var_name, var in eb.items():
        eb_value = solution.get_value(var)
        eb_values[var_name] = eb_value
    es_values = {}
    for var_name, var in es.items():
        es_value = solution.get_value(var)
        es_values[var_name] = es_value

    status = solution.solve_details.status
    objective_function = solution.objective_value

    return status, objective_function, beta, Q_values, W_values, QW_values, eb_values, es_values


def CapPolicy(CE, CEr, D, Cap, PC, PCr, SP, FC, numOfFactories, Emax, M, gamma):
    # Create a new model
    model = Model(name='Cap')

    # Define the set of factories
    factories = range(numOfFactories)

    # Define the decision variables
    beta = model.continuous_var(name='beta', lb=0)
    Q = model.continuous_var_dict(factories, name='Q')
    W = model.continuous_var_dict(factories, name='W')
    QW = model.continuous_var_dict(factories, name='QW')
    u1 = model.continuous_var_dict(factories, name='u1')
    u2 = model.continuous_var_dict(factories, name='u2')
    u3 = model.continuous_var_dict(factories, name='u3')
    u4 = model.continuous_var_dict(factories, name='u4')
    u5 = model.continuous_var_dict(factories, name='u5')
    u6 = model.continuous_var_dict(factories, name='u6')
    u7 = model.continuous_var_dict(factories, name='u7')
    u8 = model.continuous_var_dict(factories, name='u8')

    z1 = model.binary_var_dict(factories, name='z1')
    z2 = model.binary_var_dict(factories, name='z2')
    z3 = model.binary_var_dict(factories, name='z3')
    z4 = model.binary_var_dict(factories, name='z4')
    z5 = model.binary_var_dict(factories, name='z5')
    z6 = model.binary_var_dict(factories, name='z6')
    z7 = model.binary_var_dict(factories, name='z7')
    z8 = model.binary_var_dict(factories, name='z8')

    # Define the objective function
    model.minimize(gamma*sum(beta*Emax for i in factories)
                   - sum(SP[i]*Q[i]-Q[i]*PC[i]+QW[i] * (PC[i]-PCr[i])-FC[i]*W[i] for i in factories))

    model.add_constraint(beta <= 1)

    for i in factories:
        model.add_constraint(Q[i] >= D[i])
        model.add_constraint(Q[i] <= Cap[i])
        model.add_constraint(Q[i]*CE[i]+QW[i]*(CEr[i]-CE[i]) <= beta*Emax)
        model.add_constraint(QW[i] <= Q[i])
        model.add_constraint(QW[i] <= Cap[i]*W[i])
        model.add_constraint(D[i]*W[i] <= QW[i])
        model.add_constraint(W[i] <= 1)
        model.add_constraint(SP[i]-PC[i] == -u1[i]+u2[i]+CE[i]*u3[i]-u4[i])
        model.add_constraint(-FC[i] == -Cap[i]*u5[i]+D[i]*u6[i]+u7[i]-u8[i])
        model.add_constraint(
            PC[i]-PCr[i] == (CEr[i]-CE[i])*u3[i]+u4[i]+u5[i]-u6[i])
        model.add_constraint(u1[i] <= M*(1-z1[i]))
        model.add_constraint(-(D[i]-Q[i]) <= M*z1[i])
        model.add_constraint(u2[i] <= M*(1-z2[i]))
        model.add_constraint(-(Q[i]-Cap[i]) <= M*z2[i])
        model.add_constraint(u3[i] <= M*(1-z3[i]))
        model.add_constraint(-(Q[i]*CE[i]+QW[i] *
                             (CEr[i]-CE[i])-beta*Emax) <= M*z3[i])
        model.add_constraint(u4[i] <= M*(1-z4[i]))
        model.add_constraint(-(QW[i]-Q[i]) <= M*z4[i])
        model.add_constraint(u5[i] <= M*(1-z5[i]))
        model.add_constraint(-(QW[i]-Cap[i]*W[i]) <= M*z5[i])
        model.add_constraint(u6[i] <= M*(1-z6[i]))
        model.add_constraint(-(D[i]*W[i]-QW[i]) <= M*z6[i])
        model.add_constraint(u7[i] <= M*(1-z7[i]))
        model.add_constraint(-(W[i]-1) <= M*z7[i])
        model.add_constraint(u8[i] <= M*(1-z8[i]))
        model.add_constraint(W[i] <= M*z8[i])

    # Solve the model
    solution = model.solve()

    beta = solution.get_value(beta)

    Q_values = {}
    for var_name, var in Q.items():
        Q_value = solution.get_value(var)
        Q_values[var_name] = Q_value

    W_values = {}
    for var_name, var in W.items():
        W_value = solution.get_value(var)
        W_values[var_name] = W_value
    QW_values = {}
    for var_name, var in QW.items():
        QW_value = solution.get_value(var)
        QW_values[var_name] = QW_value

    status = solution.solve_details.status
    objective_function = solution.objective_value

    return status, objective_function, beta, Q_values, W_values, QW_values


def OfsetPolicy(CE, CEr, D, Cap, PC, PCr, SP, FC, numOfFactories, Emax, H, M, gamma):
    # Create a new model
    model = Model(name='Ofset')

    # Define the set of factories
    factories = range(numOfFactories)

    # Define the decision variables
    beta = model.continuous_var(name='beta', lb=0)
    Q = model.continuous_var_dict(factories, name='Q')
    W = model.continuous_var_dict(factories, name='W')
    eb = model.continuous_var_dict(factories, name='eb')
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

    z1 = model.binary_var_dict(factories, name='z1')
    z2 = model.binary_var_dict(factories, name='z2')
    z3 = model.binary_var_dict(factories, name='z3')
    z4 = model.binary_var_dict(factories, name='z4')
    z5 = model.binary_var_dict(factories, name='z5')
    z6 = model.binary_var_dict(factories, name='z6')
    z7 = model.binary_var_dict(factories, name='z7')
    z8 = model.binary_var_dict(factories, name='z8')
    z9 = model.binary_var_dict(factories, name='z9')

    # Define the objective function
    model.minimize(gamma*sum(beta*Emax
                   for i in factories)+gamma*sum(eb[i] for i in factories)
                   - sum(SP[i]*Q[i]-Q[i]*PC[i]+QW[i] *
                         (PC[i]-PCr[i])-FC[i]*W[i] for i in factories)
                   + sum(eb[i]*H for i in factories))

    model.add_constraint(beta <= 1)

    for i in factories:
        model.add_constraint(Q[i] >= D[i])
        model.add_constraint(Q[i] <= Cap[i])
        model.add_constraint(
            Q[i]*CE[i]+QW[i]*(CEr[i]-CE[i]) <= beta*Emax+eb[i])
        model.add_constraint(QW[i] <= Q[i])
        model.add_constraint(QW[i] <= Cap[i]*W[i])
        model.add_constraint(D[i]*W[i] <= QW[i])
        model.add_constraint(W[i] <= 1)
        model.add_constraint(SP[i]-PC[i] == -u1[i]+u2[i]+CE[i]*u3[i]-u4[i])
        model.add_constraint(-FC[i] == -Cap[i]*u5[i]+D[i]*u6[i]+u7[i]-u8[i])
        model.add_constraint(
            PC[i]-PCr[i] == (CEr[i]-CE[i])*u3[i]+u4[i]+u5[i]-u6[i])
        model.add_constraint(-H == -u3[i]-u9[i])
        model.add_constraint(u1[i] <= M*(1-z1[i]))
        model.add_constraint(-(D[i]-Q[i]) <= M*z1[i])
        model.add_constraint(u2[i] <= M*(1-z2[i]))
        model.add_constraint(-(Q[i]-Cap[i]) <= M*z2[i])
        model.add_constraint(u3[i] <= M*(1-z3[i]))
        model.add_constraint(-(Q[i]*CE[i]+QW[i] *
                             (CEr[i]-CE[i])-beta*Emax-eb[i]) <= M*z3[i])
        model.add_constraint(u4[i] <= M*(1-z4[i]))
        model.add_constraint(-(QW[i]-Q[i]) <= M*z4[i])
        model.add_constraint(u5[i] <= M*(1-z5[i]))
        model.add_constraint(-(QW[i]-Cap[i]*W[i]) <= M*z5[i])
        model.add_constraint(u6[i] <= M*(1-z6[i]))
        model.add_constraint(-(D[i]*W[i]-QW[i]) <= M*z6[i])
        model.add_constraint(u7[i] <= M*(1-z7[i]))
        model.add_constraint(-(W[i]-1) <= M*z7[i])
        model.add_constraint(u8[i] <= M*(1-z8[i]))
        model.add_constraint(W[i] <= M*z8[i])
        model.add_constraint(u9[i] <= M*(1-z9[i]))
        model.add_constraint(eb[i] <= M*z9[i])

    # Solve the model
    solution = model.solve()

    beta = solution.get_value(beta)

    Q_values = {}
    for var_name, var in Q.items():
        Q_value = solution.get_value(var)
        Q_values[var_name] = Q_value

    W_values = {}
    for var_name, var in W.items():
        W_value = solution.get_value(var)
        W_values[var_name] = W_value
    QW_values = {}
    for var_name, var in QW.items():
        QW_value = solution.get_value(var)
        QW_values[var_name] = QW_value
    eb_values = {}
    for var_name, var in eb.items():
        eb_value = solution.get_value(var)
        eb_values[var_name] = eb_value

    status = solution.solve_details.status
    objective_function = solution.objective_value

    return status, objective_function, beta, Q_values, W_values, QW_values, eb_values


def TaxPolicy(CE, CEr, D, Cap, PC, PCr, SP, FC, numOfFactories, tax, gamma):
    # Create a new model
    model = Model(name='Tax')

    # Define the set of factories
    factories = range(numOfFactories)

    # Define the decision variables
    Q = model.continuous_var_dict(factories, name='Q')
    W = model.continuous_var_dict(factories, name='W')
    QW = model.continuous_var_dict(factories, name='QW')

    # Define the objective function
    model.maximize(sum(SP[i]*Q[i]-Q[i]*PC[i]+QW[i] *
                       (PC[i]-PCr[i])-FC[i]*W[i] for i in factories)
                   - tax * sum(Q[i]*CE[i]+QW[i]*(CEr[i]-CE[i]) for i in factories))

    for i in factories:
        model.add_constraint(Q[i] >= D[i])
        model.add_constraint(Q[i] <= Cap[i])
        model.add_constraint(QW[i] <= Q[i])
        model.add_constraint(QW[i] <= Cap[i]*W[i])
        model.add_constraint(D[i]*W[i] <= QW[i])
        model.add_constraint(W[i] <= 1)

    # Solve the model
    solution = model.solve()

    Q_values = {}
    for var_name, var in Q.items():
        Q_value = solution.get_value(var)
        Q_values[var_name] = Q_value

    W_values = {}
    for var_name, var in W.items():
        W_value = solution.get_value(var)
        W_values[var_name] = W_value
    QW_values = {}
    for var_name, var in QW.items():
        QW_value = solution.get_value(var)
        QW_values[var_name] = QW_value

    status = solution.solve_details.status
    secondLevel_function = solution.objective_value
    objective_function = gamma * sum(Q_values[i]*CE[i]+QW_values[i]*(CEr[i]-CE[i]) for i in factories) - sum(
        SP[i] * Q_values[i]-Q_values[i]*PC[i]+QW_values[i] * (PC[i]-PCr[i])-FC[i]*W_values[i]for i in factories)

    return status, objective_function, Q_values, W_values, QW_values, secondLevel_function

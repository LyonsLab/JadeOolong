__author__ = 'senorrift'

def generate_histogram(histo_data):
    #Log Transform
    mean_logged = [math.log(x, 10) for x in histo_data['Ks']['mean']]
    xy_logged = [math.log(x, 10) for x in histo_data['Ks']['xy']]
    xz_logged = [math.log(x, 10) for x in histo_data['Ks']['xz']]
    yz_logged = [math.log(x, 10) for x in histo_data['Ks']['yz']]

    mean_layer = Histogram(
        x=mean_logged,
        opacity=0.75,
        name='Mean'
    )
    xy_layer = Histogram(
        x=xy_logged,
        opacity=0.75,
        name='Chicken-Human'
    )
    xz_layer = Histogram(
        x=xz_logged,
        opacity=0.75,
        name='Chicken-Mouse'
    )
    yz_layer = Histogram(
        x=yz_logged,
        opacity=0.75,
        name='Human-Mouse'
    )
    data = Data([mean_layer, xy_layer, xz_layer, yz_layer])
    layout = Layout(
        title="Ks Values",
        barmode='overlay'
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Ks Histogram')
    #plot_url = py.plot(data, filename='Ks Histogram')
    print plot_url
    return histo_data


def generate_histogram(histo_data):
    histogram_dict = {'values': hist_data,
                      'logten': {}}
    #Log Transform
    Ks_logged = [math.log(x, 10) for x in histo_data['Ks']['mean']]
    Kn_logged = [math.log(x, 10) for x in histo_data['Kn']['mean']]
    #KnKs_logged = [Kn/Ks for (Kn,Ks) in zip(Kn_logged, Ks_logged)]

    Ks_layer = Histogram(
        x=Ks_logged,
        opacity=0.75,
        name='Ks'
    )
    Kn_layer = Histogram(
        x=Kn_logged,
        opacity=0.75,
        name='Kn'
    )
    #KnKs_layer = Histogram(
    #    x=KnKs_logged,
    #    opacity=0.75,
    #    name='Chicken-Mouse'
    #)
    data = Data([Ks_layer, Kn_layer])
    layout = Layout(
        title="Mean Ks and Kn for Three-Way Matches between Chicken, Human, and Mouse",
        barmode='overlay',
        xaxis=XAxis(title='Log10() Value'),
        yaxis=YAxis(title='Counts')
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Ks, Kn, Histogram')
    print plot_url
    return histo_data


def generate_histogram(histo_data):
    # Log transform data
    log_data = {}
    for calculation in histo_data:
        log_data[calculation] = {}
        for comparison in histo_data[calculation]:
            log_data[calculation][comparison] = [math.log(x, 10) for x in histo_data[calculation][comparison]]

    # Build final histogram dictionary
    histogram_dict = {'values': histo_data,
                      'logten': log_data}



    #Log Transform
    cont_Ks_logged = [math.log(x, 10) for x in histo_data['Ks']['mean']]
    cont_Kn_logged = [math.log(x, 10) for x in histo_data['Kn']['mean']]
    cont_Ks_layer = Histogram(
        x=cont_Ks_logged,
        opacity=0.75,
        name='Ks'
    )
    cont_Kn_layer = Histogram(
        x=cont_Kn_logged,
        opacity=0.75,
        name='Kn'
    )
    cont_data = Data([cont_Ks_layer, cont_Kn_layer])
    cont_layout = Layout(
        title="Control",
        barmode='overlay',
        xaxis=XAxis(title='Log10() Value'),
        yaxis=YAxis(title='Counts')
    )
    cont_fig = Figure(data=cont_data, layout=cont_layout)
    cont_plot_url = py.plot(cont_fig, filename='KsKn Control')
    print "Control Plot URL: %s" % cont_plot_url

    expt_Ks_layer = Histogram(
        x=histogram_dict['logten']['Ks']['mean'],
        opacity=0.75,
        name="Ks"
    )
    expt_Kn_layer = Histogram(
        x=histogram_dict['logten']['Kn']['mean'],
        opacity=0.75,
        name="Kn"
    )
    expt_data = Data([expt_Ks_layer, expt_Kn_layer])
    expt_layout = Layout(
        title="Experimental",
        barmode='overlay',
        xaxis=XAxis(title='Log10() Value'),
        yaxis=YAxis(title='Counts')
    )
    expt_fig = Figure(data=expt_data, layout=expt_layout)
    expt_plot_url = py.plot(expt_fig, filename="KsKn Experimental")
    print "Experimental Plot URL: %s" % expt_plot_url

    return histogram_dict
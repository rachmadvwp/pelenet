import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import warnings

"""
@desc: Plot spike train of neurons in reservoir
"""
def reservoirSpikeTrain(self, fr=0, to=None):
    # Spikes from activites
    exSpikes = self.obj.exSpikeTrains if self.p.isExSpikeProbe else None
    inSpikes = 2*self.obj.inSpikeTrains if self.p.isInSpikeProbe else None  # multiply by 2 to enable a different color in imshow

    # If no spike probe is in use and we can stop here
    if (not self.p.isExSpikeProbe) and (not self.p.isInSpikeProbe):
        warnings.warn("No spikes were probed, spike trains cannot be shown.")
        return

    # Combine ex and in spikes
    allSpikes = None
    if self.p.isExSpikeProbe and self.p.isInSpikeProbe:
        allSpikes = np.vstack((exSpikes, inSpikes))
    elif self.p.isExSpikeProbe:
        allSpikes = exSpikes
    elif self.p.isInSpikeProbe:
        allSpikes = inSpikes

    # Choose spikes ("zoom" in time)
    chosenSpikes = allSpikes[:, fr:to]

    # Define colors
    cmap = colors.ListedColormap(['white', 'red', 'blue'])

    # Plot spike train
    #events = [np.where(inExp.net.exSpikeTrains[i,:])[0] for i in range(3600)]
    #plt.figure(figsize=(16, 10))
    #plt.title('Reservoir spikes')
    #plt.xlabel('Time')
    #plt.ylabel('# neuron')
    #plt.eventplot(events, color='red')
    #p = plt.show()

    # Plot spike train
    plt.figure(figsize=(16, 10))
    plt.imshow(chosenSpikes, cmap=cmap, vmin=0, vmax=2, aspect='auto')
    plt.title('Reservoir spikes')
    plt.xlabel('Time')
    plt.ylabel('# neuron')
    plt.savefig(self.plotDir + 'spikes_raster.png')
    p = plt.show()

"""
@desc: Plot average firing rate of reservoir neurons
"""
def reservoirRates(self):
    # Calculate mean rate for every simulation step
    meanRateEx = np.mean(self.obj.exSpikeTrains, axis=0) if self.p.isExSpikeProbe else None
    meanRateIn = np.mean(self.obj.inSpikeTrains, axis=0) if self.p.isInSpikeProbe else None

    # If no spike probe is in use and we can stop here
    if (not self.p.isExSpikeProbe) and (not self.p.isInSpikeProbe):
        warnings.warn("No spikes were probed, reservoir rates cannot be shown.")
        return

    # Concatenate ex and in spikes
    meanRate = None
    if self.p.isExSpikeProbe and self.p.isInSpikeProbe:
        meanRate = np.concatenate((meanRateEx, meanRateIn))
    elif self.p.isExSpikeProbe:
        meanRate = meanRateEx
    elif self.p.isInSpikeProbe:
        meanRate = meanRateIn

    # Calculate mean rate for whole simulation, except cue steps
    totalMeanRate = np.round(np.mean(meanRate[self.p.cueSteps:])*1000)/1000

    # Plot mean rate and show total mean rate in title
    plt.figure(figsize=(16, 4))
    plt.ylabel('Mean firing rate')
    plt.xlabel('Time')
    plt.title('Mean firing rate: {}'.format(totalMeanRate))
    if meanRateIn is not None:
        plt.plot(np.arange(self.p.totalSteps), meanRateIn, alpha=0.75, color='b', label='Inhibitory neurons')
    if meanRateEx is not None:
        plt.plot(np.arange(self.p.totalSteps), meanRateEx, alpha=0.75, color='r', label='Excitatory neurons')
    plt.legend()
    plt.savefig(self.plotDir + 'spikes_rates.png')
    p = plt.show()

"""
@desc: Plot spikes of noise neurons
"""
def noiseSpikes(self):
    plt.figure(figsize=(16, 4))
    plt.title('Noise spikes')
    plt.savefig(self.plotDir + 'spikes_noise.png')
    p = plt.imshow(self.obj.noiseSpikes, cmap='Greys', aspect='auto')

"""
@desc: Plot autocorreltaion function
"""
def autocorrelation(spikes, numNeuronsToShow=3):
    for i in range(numNeuronsToShow):
        result = np.array([cor(spikes[i,:-t], spikes[i,t:]) for t in range(1,101)])
        plt.figure(figsize=(16, 4))
        plt.plot(np.arange(result.shape[0]), result, linestyle='-', marker='.')
        plt.title('Autocorrelation')
        plt.xlabel('$\Delta t$')
        plt.ylabel('ACF')
        plt.savefig(self.plotDir + 'spikes_autocorrelation.png')
        p = plt.show()

"""
@desc: Plot crosscorreltaion function
"""
def crosscorrelation(spikes):
    # Get number of neurons and define crosscorrelation array
    n = spikes.shape[0]
    crosscor = np.zeros((n,n))

    # Loop throught spikes numbers
    for i in range(n):
        for j in range(n):
            # Calculate normalized cross correlations between spike trains
            crosscor[i,j] = cor(spikes[i,:], spikes[j,:])

            # TODO: Use single network instead of mean
            # Are the lines the neurons where the cue comes in?

    # Plot cross correlation matrix
    plt.imshow(crosscor)
    plt.title('Crosscorrelation')
    plt.colorbar()
    plt.savefig(self.plotDir + 'spikes_crosscorrelation.png')
    p = plt.show()

"""
@desc: Plot first 2 dimensions of PCA
"""
def pca(spikes):
    # Perform PCA
    res = self.obj.utils.pca(spikes.T.astype(float))

    # Get components from result
    comps = res[0]

    # Plot first 2 dimensions
    plt.plot(comps[:,0], comps[:,1])
    plt.title('PCA')
    plt.savefig(self.plotDir + 'spikes_pca.png')
    p = plt.show()

"""
@desc: Plot spike missmatches
"""
def spikesMissmatch(self, trainSpikes, testSpikes, windowSize = 20):
    n = self.p.reservoirExSize
    T = self.p.simulationSteps
    numSteps = int(T/windowSize)

    spikeMissmatches = np.zeros((self.p.trainingTrials, numSteps))
    # Caclulate missmatch between test and every training trial
    for i in range(self.p.trainingTrials):
        # Calculate the missmatch for every window
        for j in range(numSteps):
            # Define start and end point of window (from/to)
            fr, to = int(j*windowSize), int((j+1)*windowSize)
            # Calculate missmatch between spiking arrays
            spikeMissmatches[i,j] = np.sum(trainSpikes != testSpikes)/(windowSize*n)

    # Plot missmatch for every training trial
    plt.figure(figsize=(16, 4))
    plt.xlabel('Time')
    plt.ylabel('% of missmatching spikes')
    plt.title('Training trials compared with test trial')
    plt.ylim((-0.05,0.55))
    for i in range(self.p.trainingTrials):
        plt.plot(np.arange(0, T, windowSize), spikeMissmatches[i,:])
    plt.savefig(self.plotDir + 'spikes_missmatch.png')
    p = plt.show()

"""
@desc: Plot fano factors of spike counts
"""
"""
@desc: Fano factors of spike counts
"""
def ffSpikeCounts(spikes, neuronIdx, windowSize = 50):
    numSteps = int(spikes.shape[1]/windowSize)
    fanoFactors = []

    # Loop over all windows
    for i in range(numSteps):
        # Define starting and end point of window
        fr, to = int(i*windowSize), int((i+1)*windowSize)
        # Calculate variance and mean of spike train for specific window
        var = np.var(spikes[neuronIdx,fr:to], axis=1)
        mean = np.mean(spikes[neuronIdx,fr:to], axis=1)
        # Append fano factor to list
        fanoFactors.append(var/mean)
        
    # Make numpy array
    fanoFactors =  np.array(fanoFactors)

    # Define x for plotting
    x = np.arange(0, fanoFactors.shape[0]*windowSize, windowSize)

    # Plot fano factor for every chosen neuron
    plt.figure(figsize=(16, 4))
    for i in range(fanoFactors.shape[1]):
        labelTxt = 'Neuron '+str(neuronIdx[i])
        plt.plot(x, fanoFactors[:,i], marker='.', label=labelTxt)
    plt.xlabel('Time')
    plt.ylabel('F')
    plt.ylim((0,1))
    plt.legend()
    plt.title('Fano factors for test run')
    plt.savefig(self.plotDir + 'spikes_fanofactors.png')
    p = plt.show()

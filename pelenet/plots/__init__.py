from ..system import System
from matplotlib import rcParams

"""
@desc: Class for plotting and visualisation of network and experiment data
"""
class Plot():

    """
    @desc: Initiates plot object, gets relation to another object for getting the data
    """
    def __init__(self, rel):
        # Get system instance
        system = System.instance()

        # Store related object
        self.obj = rel
        self.p = rel.p
        self.plotDir = system.datalog.dir + 'plots/'

        # Define plot style
        self.defineStyle()

    def defineStyle(self):
        rcParams['font.family'] = self.p.pltFontFamily
        rcParams['font.size'] = self.p.pltFontSize
        rcParams['text.color'] = self.p.pltColor
        rcParams['axes.edgecolor'] = self.p.pltColor
        rcParams['xtick.color'] = self.p.pltColor
        rcParams['ytick.color'] = self.p.pltColor
        #rcParams['axes.grid'] = True
        #rcParams['grid.linestyle'] = ':'
        #rcParams['grid.linewidth'] = 0.5
        #rcParams['grid.color'] = self.p.pltColor
        rcParams['legend.fancybox'] = self.p.pltLegendFancybox
        rcParams['legend.framealpha'] = self.p.pltLegendFramealpha
        rcParams['patch.linewidth'] = self.p.pltPatchLinewidth
        #rcParams['figure.autolayout'] = True
        rcParams['savefig.format'] = self.p.pltFileType

    """
    @note: Import functions from files
    """
    # Functions to evaluate spikes
    from .spikes import (
        reservoirSpikeTrain, outputSpikeTrain, reservoirRates, noiseSpikes, pca,
        autocorrelation, crosscorrelation, spikesMissmatch, ffSpikeCounts,
        meanTopologyActivity
    )
    # Functions to evaluate weights
    from .weights import (
        initialExWeightDistribution, trainedExWeightDistribution,
        initialExWeightMatrix, trainedExWeightMatrix, weightsSortedBySupport,
        cueWeightMean
    )
    # Other functions
    from .misc import (
        preSynapticTrace, landscape
    )

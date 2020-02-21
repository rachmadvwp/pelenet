import nxsdk.api.n2a as nx
from types import SimpleNamespace
import numpy as np
import logging

# Importing own modules
from ..utils import Utils
from ..plots import Plot
from ..parameters import Parameters

"""
@desc: Reservoir network
"""
class ReservoirNetwork():

    """
    @desc: Initiates the innate network
    """
    def __init__(self, parameters=None):
        # Get parameters
        self.p = Parameters() if parameters is None else parameters

        # Set seed
        if self.p.seed is not None:
            np.random.seed(self.p.seed)

        # Instanciate nx net object
        self.nxNet = nx.NxNet()

        # Define prototypes
        #self.neuronCompProto = nx.CompartmentPrototype(compartmentVoltageDecay=20, refractoryDelay=2)  # compartment prototype (default neuron)
        self.exConnProto = nx.ConnectionPrototype(signMode=nx.SYNAPSE_SIGN_MODE.EXCITATORY, numTagBits=0, numDelayBits=0, numWeightBits=8)  # excitatory connection prototype
        self.inConnProto = nx.ConnectionPrototype(signMode=nx.SYNAPSE_SIGN_MODE.INHIBITORY, numTagBits=0, numDelayBits=0, numWeightBits=8)  # inhibitory connection prototype
        self.mixedConnProto = nx.ConnectionPrototype(signMode=nx.SYNAPSE_SIGN_MODE.MIXED)  # mixed connection prototype

        """
        Network objects
        """
        # Weights
        self.initialMasks = SimpleNamespace(**{
            'exex': None, 'inin': None, 'inex': None, 'exin': None
        })

        self.initialWeights = SimpleNamespace(**{
            'exex': None, 'inin': None, 'inex': None, 'exin': None
        })
        self.trainedWeightsExex = None

        # NxSDK compartment group chunks
        self.exReservoirChunks = []
        self.inReservoirChunks = []
        self.outputLayerChunks = []
        self.connectionChunks = []

        # Probes
        self.exSpikeProbes = []
        self.inSpikeProbes = []
        self.outSpikeProbes = []
        self.exVoltageProbes = []
        self.inVoltageProbes = []
        self.outVoltageProbes = []
        self.exCurrentProbes = []
        self.inCurrentProbes = []
        self.weightProbes = []

        # Output
        self.outputMask = None
        self.outputWeights = None

        # Spikes
        self.exSpikeTrains = []
        self.inSpikeTrains = []
        self.outSpikeTrains = []

        # Voltages
        self.outVoltageTrains = []

        # Trace input
        self.traceSpikes = []
        self.traceMasks = []
        self.traceWeights = []

        # Cue input
        self.cueSpikes = []
        self.cue = None
        self.cueWeights = None

        # Noise input spikes
        self.noiseSpikes = None
        self.noiseWeights = None

        # Instantiate utils and plot
        self.utils = Utils.instance()
        self.plot = Plot(self)

    """
    @note: Import functions from files
    """
    from .connect import addReservoirNetworkDistributed
    from .input import addCueGenerator, addRepeatedInputGenerator, addTraceGenerator
    from .noise import addNoiseGenerator, addConstantGenerator
    from .output import drawOutputMaskAndWeights
    from .probes import addProbes, postProcessing
    from .reservoir import run, build, addStopGenerator, addRepeatedStopGenerator
    from .weights import (
        drawAndSetSparseReservoirWeightMatrix, drawSparseWeightMatrix,
        drawAndSetSparseReservoirMaskMatrix, drawSparseMaskMatrix,
        getMaskedWeights, getWeightMatrixFromProbe
    )

import jpype
import jpype.imports
from jpype.types import *

# Launch the JVM
jpype.startJVM(classpath=['/home/usuario/PycharmProjects/RecSysExp/src/jython/RankSys-novelty-0.4.3.jar'])

# import the Java modules
EILD = JClass('es.uam.eps.ir.ranksys.diversity.distance.metrics.EILD')

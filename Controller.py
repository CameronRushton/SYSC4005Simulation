import logging
from Inspector import Inspector
import WorkstationFactory
import numpy as np
from Monitor import Monitor
from Type import Type


def run():
    # Initialization
    seed = 1
    np.random.seed(seed)

    logging.basicConfig(format="%(levelname)s: %(relativeCreated)6d %(threadName)s %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
    logger = logging.getLogger(__name__)
    workstations = WorkstationFactory.create_all_workstations()
    monitor = Monitor().get_instance()
    inspector_one = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.ONE])
    inspector_two = Inspector(known_workstations=workstations, seed=seed, my_types=[Type.TWO, Type.THREE])

    # We need workstations to constantly monitor their buffers and make products
    # We need the inspectors to constantly grab components and put them in the workstation buffer
    # Start threads
    for workstation in workstations:
        logger.info("Started workstation thread %s", workstation)
        workstation.start()
    inspector_one.start()
    logger.info("Started inspector thread %s", inspector_one)
    inspector_two.start()
    logger.info("Started inspector thread %s", inspector_two)

    # Keep main thread alive - daemon threads above will terminate on termination of main, non-daemon thread
    while True:
        pass


if __name__ == "__main__":
    run()

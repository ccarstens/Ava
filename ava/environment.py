from env import *
from log import log_environment as log
from ava.avaagent import AvaAgent
from ava.usercontroller import UserController
from multiprocessing import Process, Queue
from ava.nlpcontroller import NLPController
from ava.utterancedb import UtteranceDB
from ava.exceptions import MissingAvaExcpetion

class Environment:
    def __init__(self, agent_jid, user_controller_jid):
        log.debug("environment init")

        self.ava_jid = agent_jid
        self.user_jid = user_controller_jid

        self.ava = None
        self.user = None
        self.io = None
        self.nlpc = None
        self.io_process = None
        self.io_queue_in = None
        self.io_queue_out = None

        self.db = None

    def run_once(self):
        """mostly for testing features"""



    def setup(self):
        log.debug("setting up environment")
        self.setup_db()
        self.setup_io_process()
        self.setup_nlpc()
        self.setup_ava()
        self.setup_user()

        self.setup_exit()

        self.ava.bdi.set_singleton_belief("started", "yes")
        self.ava.bdi.add_achievement_goal("main")
        # self.ava.bdi.add_achievement_goal("capture_user_speech")


    def stop(self):
        log.debug("stopping environment")
        self.ava.stop()
        self.user.stop()

        self.db.stop()

    def setup_nlpc(self):
        self.nlpc = NLPController()

    def setup_ava(self):
        self.ava = AvaAgent(self.ava_jid, "ava", ASL_AVA)
        future_a = self.ava.start()
        future_a.result()
        self.ava.bdi.set_singleton_belief("usercontroller", self.user_jid)


    def setup_user(self):
        self.user = UserController(self.user_jid, "ava", ASL_USER, self.io_queue_in, self.io_queue_out, self.nlpc, self.db)
        if self.ava:
            self.user.ava = self.ava
        else:
            raise MissingAvaExcpetion

        future_u = self.user.start()
        future_u.result()
        self.user.bdi.set_singleton_belief("ava", self.ava_jid)

    def setup_io_process(self):
        self.io_queue_in = Queue()
        self.io_queue_out = Queue()
        self.io_queue_in.identifier = "io-queue-in"
        self.io_queue_out.identifier = "io-queue-out"
        self.io_process = Process(target=self.io_worker, name="io-process", daemon=True, args=(self.io_queue_in, self.io_queue_out))
        self.io_process.start()

    def setup_db(self):
        self.db = UtteranceDB(UTTERANCE_DB_FILE)
        self.db.setup()

    def io_worker(self, queue_in: Queue, queue_out: Queue):
        from ava.iocontroller import IOController
        from log import log_ioprocess as log
        log.debug("IOProcess started")

        io = IOController(queue_in, queue_out)
        io.run()
        pass

    def setup_exit(self):
        import signal, sys

        def my_sig_handler(signal, frame):
            self.stop()
            log.debug("received interrupt signal")
            sys.exit(0)
        signal.signal(signal.SIGINT, my_sig_handler)


import unittest

from reptor.lib.reptor import Reptor
from reptor.lib.errors import MissingArgumentError

from ..NotesAPI import NotesAPI


class TestNotesAPI(unittest.TestCase):
    def setUp(self):
        self.reptor = Reptor()

    def test_notes_api_init(self):
        # Test valid private note
        self.reptor._config._raw_config['server'] = 'https://demo.sysre.pt'
        self.reptor._config._raw_config['cli'] = {'private_note': True}
        try:
            n = NotesAPI(reptor=self.reptor)
            self.assertTrue(n.private_note)
        except (ValueError, MissingArgumentError):
            self.fail("NotesAPI raised Error")

        # Test valid project note
        self.reptor._config._raw_config['server'] = 'https://demo.sysre.pt'
        self.reptor._config._raw_config['cli'] = {'private_note': False}
        self.reptor._config._raw_config['project_id'] = '2b5de38d-2932-4112-b0f7-42c4889dd64d'
        try:
            n = NotesAPI(reptor=self.reptor)
            self.assertFalse(n.private_note)
        except (ValueError, MissingArgumentError):
            self.fail("NotesAPI raised Error")

        # Test missing project id and missing private_note
        self.reptor._config._raw_config['server'] = 'https://demo.sysre.pt'
        self.reptor._config._raw_config['cli'] = {'private_note': False}
        self.reptor._config._raw_config['project_id'] = ''
        with self.assertRaises(MissingArgumentError):
            NotesAPI(reptor=self.reptor)

        # Test missing server
        self.reptor._config._raw_config['server'] = ''
        self.reptor._config._raw_config['cli'] = {'private_note': True}
        with self.assertRaises(ValueError):
           NotesAPI(reptor=self.reptor)
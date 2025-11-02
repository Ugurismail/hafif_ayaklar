# Core views package
# This file imports all views from modularized files
# Allows backward compatibility with: from core.views import *

# Import from modular files
from .auth_views import *
from .user_views import *
from .question_views import *
from .answer_views import *
from .message_views import *
from .vote_save_views import *
from .random_sentence_views import *
from .definition_reference_views import *
from .poll_views import *
from .iat_views import *
from .kenarda_views import *
from .cikis_test_views import *
from .delphoi_views import *
from .hashtag_views import *
from .misc_views import *

# Legacy file kept as backup (can be removed after verification)
# from ._legacy import *

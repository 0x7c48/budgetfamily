#!/usr/bin/env python
# coding=utf-8

import os
import IPython

from flask import *
from budgetfamily import app, db, user_datastore
from budgetfamily.auth.models import *


IPython.embed(header='IPython')

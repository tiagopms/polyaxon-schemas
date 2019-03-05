# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.cached_property import cached_property

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.notebook import NotebookConfig
from polyaxon_schemas.specs.base import BaseSpecification
from polyaxon_schemas.specs.build import BuildSpecification


class NotebookSpecification(BuildSpecification):
    """The polyaxonfile specification for notebooks.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._NOTEBOOK  # pylint:disable=protected-access
    ENVIRONMENT_CONFIG = NotebookConfig

    def _extra_validation(self):
        try:
            super(NotebookSpecification, self)._extra_validation()
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'NotebookSpecification must contain a valid `build` section.')

    @cached_property
    def backend(self):
        if self.environment:
            return self.environment.backend
        return None
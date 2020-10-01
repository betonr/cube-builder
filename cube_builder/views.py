#
# This file is part of Python Module for Cube Builder.
# Copyright (C) 2019-2020 INPE.
#
# Cube Builder is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Define Brazil Data Cube Cube Builder routes."""

# 3rdparty
from flask import Blueprint, request

# Cube Builder
from .version import __version__
from .controller import CubeController
from .forms import GridRefSysForm, DataCubeForm, DataCubeProcessForm, PeriodForm


bp = Blueprint('cubes', import_name=__name__)

@bp.route('/', methods=['GET'])
def status():
    return dict(
        message = 'Running',
        description = 'Cube Builder',
        version = __version__
    ), 200


@bp.route('/create-cube', methods=['POST'])
def create_cube():
    """Define POST handler for datacube creation.

    Expects a JSON that matches with ``DataCubeForm``.
    """
    form = DataCubeForm()

    args = request.get_json()

    errors = form.validate(args)

    if errors:
        return errors, 400

    data = form.load(args)

    cubes, status = CubeController.create(data)

    return cubes, status


@bp.route('/start-cube', methods=['POST'])
def start_cube():
    """Define POST handler for datacube execution.

    Expects a JSON that matches with ``DataCubeProcessForm``.
    """
    args = request.get_json()

    form = DataCubeProcessForm()

    data = form.load(args)

    proc = CubeController.maestro(**data)

    return proc


@bp.route('/list-merges', methods=['GET'])
def list_merges():
    """Define POST handler for datacube execution.

    Expects a JSON that matches with ``DataCubeProcessForm``.
    """
    args = request.args

    res = CubeController.check_for_invalid_merges(**args)

    return res


@bp.route('/create-temporal-schema', methods=['POST'])
def temporal_schema():
    """Create the temporal composite schema using HTTP Post method.

    Expects a JSON that matches with ``TemporalSchemaParser``.
    """

    args = request.get_json()

    errors = form.validate(args)

    if errors:
        return errors, 400

    cubes, status = CubeController.create_temporal_composition(args)

    return cubes, status


@bp.route('/create-grs', methods=['POST'])
def create_grs():
    """Create the grid reference system using HTTP Post method."""
    form = GridRefSysForm()

    args = request.get_json()

    errors = form.validate(args)

    if errors:
        return errors, 400

    cubes, status = CubeController.create_grs_schema(**args)

    return cubes, status


@bp.route('/list-periods', methods=['POST'])
def list_periods():
    """List data cube periods.

    The user must provide the following query-string parameters:
    - schema: Temporal Schema
    - step: Temporal Step
    - start_date: Start offset
    - last_date: End date offset
    """
    parser = PeriodForm()

    args = request.args

    errors = parser.validate(args)

    if errors:
        return errors, 400

    return CubeController.generate_periods(**args)
# coding: utf-8
import click
from sqlalchemy import create_engine


@click.command()
@click.option("--db-uri", help="database uri, used for SQLAlchemy")
def cli(db_uri):
    """
    Create all RMDB tables for NWPC Operation Systems running in HPC-URANUS and HPC-PI.
    """
    from nwpc_workflow_log_model.rmdb.base.model import Model
    from nwpc_workflow_log_model.rmdb.sms.repo import SmsRepo
    from nwpc_workflow_log_model.rmdb.ecflow.repo import EcflowRepo

    engine = create_engine(db_uri)
    Model.metadata.create_all(engine)

    from nwpc_workflow_log_model.rmdb.util.session import get_session

    session = get_session(db_uri)
    EcflowRepo.create_repo("nwp_xp", "pi_nwpc_op", session)
    EcflowRepo.create_repo("nwp_xp", "pi_nwpc_qu", session)
    EcflowRepo.create_repo("nwp_xp", "pi_nwpc_qu_eps", session)
    EcflowRepo.create_repo("nwp_xp", "pi_nwpc_pd", session)

    SmsRepo.create_repo("nwp_xp", "aix_nwpc_op", session)
    SmsRepo.create_repo("nwp_xp", "aix_nwpc_qu", session)
    SmsRepo.create_repo("nwp_xp", "aix_eps_nwpc_qu", session)
    SmsRepo.create_repo("nwp_xp", "aix_nwpc_pd", session)


if __name__ == "__main__":
    cli()

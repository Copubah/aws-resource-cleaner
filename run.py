from cleaner.cleanup import (
    stop_idle_ec2,
    delete_unused_volumes,
    delete_unused_elastic_ips,
    delete_unattached_enis,
    stop_idle_rds,
    report_idle_lambdas,
    stop_idle_ecs_services,
)

if __name__ == "__main__":
    dry_run = True  # Set to False when ready to perform actual changes

    stop_idle_ec2(dry_run=dry_run)
    delete_unused_volumes(dry_run=dry_run)
    delete_unused_elastic_ips(dry_run=dry_run)
    delete_unattached_enis(dry_run=dry_run)
    stop_idle_rds(dry_run=dry_run)
    report_idle_lambdas()
    stop_idle_ecs_services(dry_run=dry_run)

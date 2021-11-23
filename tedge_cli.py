import os
import click
from helper import ARCH_MAPPER, TEDGE_PACKAGES, create_debian_packages, checkout_branch, upload_debian_to_host, upload_debian_to_host_from_cache, cached_debian_packages, cache_debian_packages

__author__ = "initard"

@click.group()
def main():
    """
    Simple CLI for building, installing and deploying thin edge
    """
    tedge_dir = os.getenv("TEDGE_DIR", None)
    if not tedge_dir:
        raise Exception("TEDGE_DIR environment variable not set")
    pass

@main.command()
@click.option("--arch", "-a", required=True, type=str, default="x86_64", show_default=True)
@click.option("--branch",  "-b", required=False, default="main", show_default=True)
@click.option("--release", default=True, is_flag=True, show_default=True)
@click.option("--host-name", "-n", required=False, show_default=True)
@click.option("--tag", required=False)
def build(branch, arch, release, host_name, tag):
    arch = ARCH_MAPPER[arch]
    # TODO: refactor this
    if tag:
        if cached_debian_packages(tag):
            assert host_name
            # upload
            for package in TEDGE_PACKAGES:
                upload_debian_to_host_from_cache(package_name=package, host_name=host_name, tag=tag)
        else:
            checkout_branch(branch_name=branch)
            create_debian_packages(arch, release)
            for package in TEDGE_PACKAGES:
                cache_debian_packages(arch=arch, package_name=package, tag=tag)

    else:
        checkout_branch(branch_name=branch)
        arch = ARCH_MAPPER[arch]
        create_debian_packages(arch, release)


        if host_name:
            for package in TEDGE_PACKAGES:
                upload_debian_to_host(arch=arch, host_name=host_name, package_name=package)



if __name__ == "__main__":
    main()

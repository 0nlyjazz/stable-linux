#
# Description: This sets up the rust environment to compile rust modules
# Author: Sarbojit Ganguly
# Bugs/Suggestions: onlyjazz.16180@gmail.com
#

import subprocess
import argparse
import logging
import sys
import os


logging.basicConfig(format='RustEnvsetup:[%(asctime)s][%(funcName)s()][%(levelname)s]::%(message)s', level=logging.DEBUG)

cmd_pre_setup_script = "rust-env.sh"


#
# According to rust quick-start.rst document, the current rust compiler 
# which is supported is handled by min-tool-version.sh
# so we will allow that to run and handle the output.
#



def min_supported_compiler():
    logging.debug("E")
    cmd_list = ['scripts/min-tool-version.sh', 'rustc']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    # this is the minimum required rust compiler supported
    logging.info("minimum supported compiler version = %s", output)
    logging.debug("X")
    return output

def min_supported_bindgen():
    logging.debug("E")
    cmd_list = ['scripts/min-tool-version.sh', 'bindgen']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    # this is the minimum required rust bindgen supported
    logging.info("minimum supported bindgen version = %s", output)   
    logging.debug("X")
    return output

def test_rust_env():
    logging.debug("E")
    output = subprocess.check_output(['rustc', '--version'])
    # remove trailing newline
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("installed %s", output)

    output = subprocess.check_output(['bindgen', '--version'])
    # remove trailing newline
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("installed %s", output)

    min_supported_compiler()
    min_supported_bindgen()

    logging.debug("X")
    return


def system_check():
    logging.debug("E")
    cmd_list = ['make', 'arch=ARM64', 'LLVM=1', 'rustavailable']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)    

    logging.debug("X")
    return


def run_setup_min_supported_compiler_and_toolchain():
    logging.debug("E")

    minrustc = min_supported_compiler()

    # now we will supply this to the rustup override set
    cmd_list = ['rustup', 'override' , 'set', minrustc]
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)

    logging.debug("X")
    return


def run_setup_min_supported_bindgen():
    logging.debug("E")

    minbindgen = min_supported_bindgen()

    # now we will supply this value to cargo
    cmd_list = ['cargo', 'install', '--locked', '--force', '--version', minbindgen, 'bindgen']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)

    logging.debug("X")
    return

def run_add_component_src():
    logging.debug("E")

    cmd_list=['rustup', 'component', 'add', 'rust-src']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)    
    

    logging.debug("X")
    return

def run_add_component_clippy():
    logging.debug("E")

    cmd_list=['rustup', 'component', 'add', 'clippy']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)

    logging.debug("X")
    return


def run_add_component_bindgen():
    logging.debug("E")

    cmd_list=['cargo', 'install', 'bindgen-cli']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)

    logging.debug("X")
    return 

def run_rustup():

    logging.debug("E")
    cmd_rustup      = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rustup-init.sh"
    cmd_init_script = "rustup-init.sh"
    os.system(cmd_rustup)
    logging.debug("downloaded")


    #install the compiler, toolchain etc
    os.system("chmod a+x ./"+cmd_init_script)
    os.system("./"+cmd_init_script+"  -q -y")

    logging.info("default installation is done")
    logging.debug("we will run the source to bring rust to current shell...")
    os.system("./"+cmd_pre_setup_script+" cargoenv")

    logging.debug("X")
    return


def run_everything_from_top():
    logging.debug("E")
    logging.info("running pre-setup script...")
    # remove old path, if exists
    os.system("chmod a+x ./"+ cmd_pre_setup_script)
    os.system("./"+cmd_pre_setup_script+" setpath")
    
    # download, run and install rust (this will install the latest)
    # we will do customization later...
    run_rustup()

    # download and install bindgen
    run_add_component_bindgen()

    # at this point, rustup is installed so do a quick check on the shell
    test_rust_env()

    # setup min supported compiler, toolchain bindgen
    run_setup_min_supported_compiler_and_toolchain()
    run_setup_min_supported_bindgen()

    # add the components
    run_add_component_src()
    run_add_component_clippy()


    # run a system check 
    system_check()

    logging.debug("X")
    return


def uninstall_rust():
    logging.debug("E")

    cmd_list = ['rustup', 'self', 'uninstall', '-y']
    output = subprocess.check_output(cmd_list)
    output = output.decode('utf-8')
    output = output.rstrip('\n')
    logging.info("output = %s", output)

    logging.debug("X")
    return

def main():

    logging.info("E")

    parser = argparse.ArgumentParser()

    parser.add_argument('--everything', type=str, required=False)
    parser.add_argument('--testenv', type=str, required=False)
    parser.add_argument('--setupcompiler', type=str, required=False)
    parser.add_argument('--setall', type=str, required=False)
    parser.add_argument("--remove", type=str, required=False)
    parser.add_argument("--syscheck", type=str, required=False)

    args = parser.parse_args()

    if(args.everything == 'yes'):
        run_everything_from_top()
    
    if(args.testenv == 'yes'):
        test_rust_env()

    if(args.setupcompiler == 'yes'):
        run_setup_min_supported_compiler_and_toolchain()

    if(args.setall == 'yes'):
        run_setup_min_supported_compiler_and_toolchain()
        run_setup_min_supported_bindgen()

    if(args.remove == 'yes'):
        uninstall_rust()

    if(args.syscheck == 'yes'):
        system_check()
    



    logging.info("X")
    return

    
if __name__ == "__main__":
    main()
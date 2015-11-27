# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

# All Vagrant configuration is done here. The most common configuration
# options are documented and commented below. For a complete reference,
# please see the online documentation at vagrantup.com.
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  ########## BASE BOX
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  ########## END BASE BOX

  ########## FORWARDED PORTS
  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8000" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 8082, host: 8082
  ########## END FORWARDED PORTS

  ########## SHARED USER FOLDERS
  # Share two additional folders with the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "code", "/home/vagrant/code"
  config.vm.synced_folder "data", "/home/vagrant/data"
  ########## END SHARED USER FOLDERS

  ########## VIRTUALBOX VM SETTINGS
  config.vm.provider "virtualbox" do |vb|
    # Boot with headless mode, so no virtualbox window will pop up
    vb.gui = true
  
    # Use VBoxManage to customize the VM. Change the memory and the name:
    vb.customize [  "modifyvm", :id,
                    "--memory", "512",
                    "--name", "vagrant-try-luigi",
                 ]
  end
  ########## END VIRTUALBOX VM SETTINGS

  ########## SALT PROVISIONING 
  config.vm.synced_folder "salt/roots", "/srv/salt"
  config.vm.provision :salt do |salt|

    salt.minion_config = "salt/minion"
    salt.run_highstate = true
    salt.bootstrap_options = "-F -c /tmp/ -P"

  end
  ########## END SALT PROVISIONING 

end

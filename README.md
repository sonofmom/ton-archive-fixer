## Fixer for TON archival nodes database
This script will fix databases of archival nodes and inject blocks from 3.7mil to 4.9mil into global index for autoload.

All commands shown in this guide assume that you run node with mytonctrl with default locations, if your locations differ make sure to adjust the commands accordingly.

### Who needs this
Anyone who operates TON archival node that does not preload archive files of the blocks mentioned above, to check if your node is affected you can try to access block 4000000 via blockchain explorer, if get error then you need this fixer.

Another way to check if your node needs this fix is to run:

```ls -l /proc/`ps -A -o pid,cmd | grep validator-engine | grep -v grep | head -n 1 | awk '{print $1}'`/fd | grep arch0040 | wc -l```

If this returns 0 then your node needs fixing.

### Prerequesites
#### TON Binaries
Your node should run **latest** ton binaries. If you use mytonctrl, run `upgrade`, if you build your own binaries, make sure to build and install latest master.

#### RocksDB ldb binary
It is very important that you use same version of rocksDB ldb binary as the library compiled into validator-engine. You can compile it yourself by running `make` in `third-party/rocksdb/tools` of your TON build directory.

A binary of ldb built on `Ubuntu 20.04.2 LTS` is provided with this repository.

### Preparations
* Stop your node
* Make a backup or ZFS snapshot of node database

### Fix
Dump your `globalindex`
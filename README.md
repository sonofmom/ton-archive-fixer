## Fixer for TON archival nodes database
This script will fix databases of archival nodes and inject blocks from 3.7mil to 4.9mil into global index for autoload.

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
* Stop your validator service
* Make a backup or ZFS snapshot of node database

### Fix
All commands shown in this guide assume that you run node with mytonctrl with default locations, if your locations differ make sure to adjust the commands accordingly.

It is also assumed that you are located in root of this cloned repository.

#### Make a backup copy of globalindex
```sudo cp -Rp /var/ton-work/db/files/globalindex /var/ton-work/db/files/globalindex.bak```

#### Dump your node `globalindex`
```./bin/ldb --db=/var/ton-work/db/files/globalindex dump --hex > /tmp/globalindex.dump```

#### Patch the dump
```./patch_globalindex.py --dump=/tmp/globalindex.dump```

If patch was ok script will return a **SUCCESS** message.

#### Reload `globalindex` from dump
```cat /tmp/globalindex.dump | ./bin/ldb --db=/var/ton-work/db/files/globalindex load --hex --block_size=65536 --create_if_missing --disable_wal```

### Followup steps
You can start your validator service now, after start check if the node loads blocks using steps outlined in second chapter of this readme.
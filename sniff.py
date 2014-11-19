# -*- coding: utf-8 -*-
import subprocess


def count_devices(interface, server, to_remove = []):
	cmd = ["sudo", "arp-scan", "--retry=8", "--ignoredups", "-I", interface, server + "/24"]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

	out, err = p.communicate()

	hosts = out.split("\n")[2:-4]

	devices = map(lambda x: x.split("\t")[-1], hosts)


	devices = filter(lambda x: x not in to_remove, devices)
	counts  = {key: devices.count(key) for key in devices}

	return counts
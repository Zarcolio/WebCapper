#!/usr/bin/env python3

foldergits="/opt/gits"
import os
import subprocess
import socket
from contextlib import closing
import argparse

def check_socket(host, port):
	try:
		with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
			if sock.connect_ex((host, port)) == 0:
				# Port is open
				return True
			else:
				# Port is close
				return False
	except Exception:
		# Cannot reach host (dead of does not resolve)
		return False
		pass

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain.")
	parser.add_argument('-o', '--output', type=str, help="Output file.")
	return parser.parse_args()

def save_file(subdomain,output_file):
	with open(output_file,"a") as f:
		f.write(subdomain + '\n')
		f.close()

def main():
	args = parse_args()
	subdomains = []
	target = args.domain
	output = args.output

	# Create and change to new directory based on domain name
	try:
		os.mkdir(target)
	except Exception:
		pass
	os.chdir(target)

	# If target file exists remove file, because ctfr.py appends to file
	try:
		os.remove (target + "-ctfr-hosts.txt")
	except Exception:
		pass

	# Get hostnames with ctfr.py
	os.system("python "+foldergits + "/ctfr/ctfr.py -d " + target + " -o " + target + "-ctfr-hosts.txt")

	# Open output file
	with open (target + "-ctfr-hosts.txt") as ins:
		array = []
		for host in ins:
			host = host.rstrip('\n')
			host = host.replace("*.", "")
			if check_socket(host, 443):
				print ("Saving "+host)
				# Warning: cutycapt output goes to /dev/nul
				os.system("cutycapt --url=https://" + host + " --out=" + host + ".png --insecure > /dev/nul 2>&1")
			else:
				print ("Not saving "+host)


main()
	

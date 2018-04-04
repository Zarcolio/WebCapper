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
	parser.add_argument('-d', '--domain', type=str, help="Target domain.")
	parser.add_argument('-i', '--input',  type=str, help="Input file.")
	return parser.parse_args()

def webcapper(domain):
	# Create and change to new directory based on domain name
	try:
		os.mkdir(domain)
	except Exception:
		pass
	os.chdir(domain)

	# If target file exists remove file, because ctfr.py appends to file
	try:
		os.remove (domain + "-ctfr-hosts.txt")
	except Exception:
		pass

	# Get hostnames with ctfr.py
	os.system("python "+foldergits + "/ctfr/ctfr.py -d " + domain + " -o " + domain + "-ctfr-hosts.txt")

	# Open output file
	try:
		with open (domain + "-ctfr-hosts.txt") as ins:
			array = []
			for host in ins:
				host = host.rstrip('\n')
				host = host.rstrip('\r')
				host = host.replace("*.", "")
				if check_socket(host, 443):
					print ("Saving "+host)
					# Warning: cutycapt output goes to /dev/nul
					os.system("cutycapt --url=https://" + host + " --out=" + host + ".png --insecure > /dev/nul 2>&1")
				else:
					print ("Not saving "+host)
	except Exception:
		pass


def main():
	args = parse_args()
	subdomains = []
	
	if (args.domain and args.input):
		print ("Use only --domain or --input, but not both.")
		exit()

	if (not args.domain and not args.input):
		print ("")
		print ("python webcapper.py [input option]")
		print ("")
		print ("Input options are mutually exclusive:")
		print ("")
		print ("-d --domain		Enter a single domain name to webcap.")
		print ("-i --input		Enter a file name containing one or more domain names to webcap.")
		print ("")
		exit()
		
	if (args.input):
		# Create and change to new directory based on input file name
		try:
			os.mkdir(args.input+".save")
		except Exception:
			pass
		os.chdir(args.input+".save")
		
		input_file = open ("../" + args.input, "r")
		for input_domain in input_file:
			input_domain = input_domain.rstrip('\n')
			input_domain = input_domain.rstrip('\r')
			webcapper(input_domain)
			os.chdir("..")
	else:
		webcapper(args.domain)


main()
	

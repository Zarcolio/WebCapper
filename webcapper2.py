#!/usr/bin/python

foldergits="/root/subfinder/"
portlist = [80, 443]

from async_dns_capt import AsyncResolver

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

	# If target file exists remove file, because subf.py appends to file
	try:
		os.remove (domain + "-subf-hosts.txt")
	except Exception:
		pass

	# Get hostnames with subfinder
	os.system(foldergits + "subfinder -d " + domain + " -o " + domain + "-subf-hosts.txt")

	outresolved    = open(domain + "-subf-hosts-resolved.txt", "w")
	outnotresolved = open(domain + "-subf-hosts-notresolved.txt", "w")
	# Open file with hosts found
	try:
		with open (domain + "-subf-hosts.txt") as ins:
			array = []
			insdata = [line.rstrip() for line in ins]
			ar = AsyncResolver(insdata)
			resolved = ar.resolve()

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
	

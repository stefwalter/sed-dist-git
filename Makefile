# Makefile for source rpm: sed
# $Id$
NAME := sed
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common

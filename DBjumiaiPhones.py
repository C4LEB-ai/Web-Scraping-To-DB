#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:37:25 2022

@author: c4leb
"""

import psycopg2
import numpy
import psycopg2.extras as extras
import pandas as pd


def execute_values(conn, df, table):

	tuples = [tuple(x) for x in df.to_numpy()]

	cols = ','.join(list(df.columns))
	# SQL query to execute
	query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
	cursor = conn.cursor()
	try:
		extras.execute_values(cursor, query, tuples)
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print("Error: %s" % error)
		conn.rollback()
		cursor.close()
		return 1
	print("the dataframe is inserted")
	cursor.close()


conn = psycopg2.connect(
	database="postgres", user='postgres', password='<1109>', host='localhost', port='5432'
)

df = pd.read_csv('jumia phone scrape.csv')

execute_values(conn, df, 'jumia2')

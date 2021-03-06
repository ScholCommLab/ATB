# -*- coding: utf-8 -*-
"""DBConnection

This is a wrapper module for the sqlite3 and the database management for
altmetrics research at scholcommlab.ca

author: Asura Enkhbayar <asura.enkhbayar@gmail.com>
"""

import sqlite3 as lite

class DBConnection(object):
    """A helper class to manage litecon3 connection and several saving setups."""
    def __init__(self, db_path, db_table, db_col_names, db_col_types, unique_col):
        self.path = db_path
        self.table = db_table
        self.col_names = db_col_names
        self.col_types = db_col_types
        self.unique = unique_col

        col_name_type = ['{} {}'.format(n, t) for (n, t) in zip(self.col_names, self.col_types)]
        cols = ', '.join(col_name_type)

        self.litecon = lite.connect(self.path)

        with self.litecon:
            litecur = self.litecon.cursor()
            litecur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(self.table, cols))
            litecur.execute("CREATE UNIQUE INDEX IF NOT EXISTS {} ON {}({})".format(
                "_".join([self.table, self.unique]), self.table, self.unique))

    def save_row(self, row):
        '''
        Write a row
        '''
        with self.litecon:
            litecur = self.litecon.cursor()
            placeholders = ",".join([':' + col_n for col_n in self.col_names])
            row = ([row[key] for key in self.col_names])
            litecur.execute("""INSERT OR IGNORE INTO {} ({}) VALUES ({})""".format(
                self.table, ", ".join(self.col_names), placeholders), row)

    def update_row(self, row):
        '''
        Update a row
        '''
        with self.litecon:
            litecur = self.litecon.cursor()
            placeholders = ",".join([':' + col_n for col_n in self.col_names])
            row = ([row[key] for key in self.col_names])
            litecur.execute("""REPLACE INTO {} ({}) VALUES ({})""".format(
                self.table, ", ".join(self.col_names), placeholders), row)

    def select(self, columns):
        '''
        Select a single column or a list of columns
        '''
        with self.litecon:
            if isinstance(columns, list):
                litecur = self.litecon.cursor()
                litecur.execute("SELECT {} FROM {}".format(", ".join(columns), self.table))
            else:
                self.litecon.row_factory = lambda cursor, row: row[0]
                litecur = self.litecon.cursor()
                litecur.execute("SELECT {} FROM {}".format(columns, self.table))
            rows = litecur.fetchall()
            self.litecon.row_factory = lambda cursor, row: row
            return rows

#!/usr/bin/python
# -*- coding: UTF-8 -*-
from annual_report import AnnualReport


if __name__ == "__main__":
    ar = AnnualReport(github_id="JalanJiang")
    if not ar.check_user_data():
        print("查无此人")
    else:
        image = ar.draw()
        image.show()
        image.save('./img/tmp.png')
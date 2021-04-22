import gspread
from pprint import pprint
import math
import numpy as np
from replit import db
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client_sheets = gspread.authorize(creds)
sheet = client_sheets.open("Lost Tribe").worksheet("MU datas") 

def updateDatas():

  mat = np.array(db["mat"])
  deckMat = []

  for deck in db["decks"].keys():
    i = db["decks"][deck]
    denom = (np.sum(mat[i,:])+np.sum(mat[:,i])).item()
    if denom > 0:
      ratio = round(np.sum(mat[i,:])/denom,4)
    else:
      ratio = 'no data'
    
    deckMat.append([ratio, denom, deck])
    deckMat.append([ratio, denom, deck])

    try:
      sheet.update_cell(1, int(i) + 4, deck)
    except:
      pass

  matcopy = np.copy(mat)
  matcopy2 = np.copy(mat)

  [n, m] = np.shape(mat)

  #mat = mat.tolist()
  matcopy = matcopy.tolist()
  matcopy2 = matcopy2.tolist()

  for i in range(n):
    for j in range(m):
      if mat[i][j] + mat[j][i] > 0:
        matcopy[i][j] = round(mat[i][j]/(mat[i][j] + mat[j][i]),4)
      else:
        matcopy[i][j] = 'no data'

      matcopy2[i][j] = "{} - {}".format(mat[i][j], mat[j][i])


  finalMat = []
  for i in range(n):
    finalMat.append(matcopy[i])
    finalMat.append(matcopy2[i])


  sheet.update('A2', deckMat)
  sheet.update('D2', finalMat)
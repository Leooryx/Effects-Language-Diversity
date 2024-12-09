#pip install boto3


#pas nécessairement utile de télécharger AMZ CLI
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)


import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io
import os


# Ouvrir et lire le fichier .env
with open('/home/onyxia/work/Avions-Retard-et-Meteo/.env') as f:
    for line in f:
        line = line.strip()
        # Ignorer les lignes vides ou les commentaires
        if not line or line.startswith('#'):
            continue
        # Séparer la clé de la valeur (en supposant un format key=value)
        key, value = line.split('=', 1)
        os.environ[key] = value

# Maintenant que les variables sont chargées dans l'environnement, vous pouvez les récupérer
s3_access_key_id = os.getenv("S3_ACCESS_KEY_ID")
s3_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY")
print(s3_secret_access_key)


bucket_name = "avion-et-meteo"

#s3://avion-et-meteo/Data-preprocessing/

# Create a session and S3 client
session = boto3.session.Session()
s3_client = session.client(service_name='s3',
    aws_access_key_id=s3_access_key_id,
    aws_secret_access_key=s3_secret_access_key,
)

# List objects in the specific bucket
print(f"Listing objects in bucket '{bucket_name}':")
response = s3_client.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    for obj in response['Contents']:
        print(f"{obj['Key']}")
else:
    print("Bucket is empty.")



#Création d'un répertoire local pour chaque dossier contenu dans S3
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        print(f"Processing: {key}")
        
        # Créez les répertoires nécessaires localement
        if '/' in key:  # Si le chemin contient un "/", cela indique un dossier ou un chemin structuré
            local_path = os.path.dirname(key)  # Récupérer le chemin du répertoire
            if not os.path.exists(local_path):
                os.makedirs(local_path)  # Crée les dossiers si nécessaire
        
        # Télécharge uniquement si ce n'est pas un "dossier" (c'est-à-dire si Key ne se termine pas par "/")
        if not key.endswith('/'):
            s3_client.download_file(bucket_name, key, key)
else:
    print("Bucket is empty.")

def upload_to_s3(folder, file_name):
    """
    Sauvegarde un document un dossier spécifique d'un bucket S3.

    Args:
        folder (str): Le nom du dossier dans lequel enregistrer le document.
        file_name (str): Le nom du fichier à enregistrer.
    """

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Remettre le pointeur du buffer au début

    try:
        s3_client.upload_fileobj(buffer, bucket_name, f"{folder}/{file_name}")
        print(f"Le document a été chargé avec succès dans le bucket S3 '{bucket_name}' sous le nom '{file_name}'.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement : {e}")

    buffer.close()

#Partie 1.1 : Pre-processing the planes data

#Hypothèse de travail : les avions sont similairement sensibles aux mêmes variations de météo sur leur retard --> on peut généraliser la situation d'un aéroports aux autres
#On décide de se concentrer sur l'aéroport JFK dont le code est : 10135

january_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_january.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(january_JFK)) #191
february_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_february.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(february_JFK)) #128
march_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_march.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(march_JFK)) #167
april_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_april.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(april_JFK)) #139
may_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_may.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(may_JFK)) #160
june_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_june.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(june_JFK)) #134
july_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_july.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(july_JFK)) #192
september_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_september.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(september_JFK)) #206
october_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_october.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(october_JFK)) #253
november_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_november.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(november_JFK)) #220
december_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_december.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(december_JFK)) #168
#Total = 1958
year = [january_JFK, february_JFK, march_JFK, april_JFK, may_JFK, june_JFK, july_JFK, september_JFK, october_JFK, november_JFK, december_JFK]

JFK_2017 = pd.concat(year, ignore_index=True)
#print(len(JFK_2017))
print(JFK_2017.info())
#Mettre dans le bon format
JFK_2017['FL_DATE'] = pd.to_datetime(JFK_2017['FL_DATE'])
#Hypothèse : on remplace les valeurs manquantes de WEATHER_DELAY dans JFK_2017 par 0 car on suppose qu'un retard cause beaucoup de colère et donc sera noté plus fréquemment qu'une absence de retard
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)
upload_to_s3("Pre-Processed_data", "JFK_2017.csv")




#Partie 1.2 : Pre-processing the weather data

weather = pd.read_csv('Data-preprocessing/jfk_weather.csv')
print(weather.info()) #beaucoup de type ne sont pas bien définis
#90 colonnes
weather['DATE'] = pd.to_datetime(weather['DATE'])

weather_2017 = weather[weather['DATE'].dt.year == 2017]
#print(weather_2017.head())
#print(weather_2017.tail())

# Dictionnaire pour mapper les colonnes avec leur type attendu
column_types = {
    # Float64
    'ELEVATION': 'float64',
    'LATITUDE': 'float64',
    'LONGITUDE': 'float64',
    'HOURLYWindGustSpeed': 'float64',
    'HOURLYPressureTendency': 'float64',
    'DAILYMaximumDryBulbTemp': 'float64',
    'DAILYMinimumDryBulbTemp': 'float64',
    'DAILYAverageDryBulbTemp': 'float64',
    'DAILYDeptFromNormalAverageTemp': 'float64',
    'DAILYAverageRelativeHumidity': 'float64',
    'DAILYAverageDewPointTemp': 'float64',
    'DAILYAverageWetBulbTemp': 'float64',
    'DAILYHeatingDegreeDays': 'float64',
    'DAILYCoolingDegreeDays': 'float64',
    'DAILYAverageStationPressure': 'float64',
    'DAILYAverageSeaLevelPressure': 'float64',
    'DAILYAverageWindSpeed': 'float64',
    'DAILYPeakWindSpeed': 'float64',
    'PeakWindDirection': 'float64',
    'DAILYSustainedWindSpeed': 'float64',
    'DAILYSustainedWindDirection': 'float64',
    'MonthlyMaximumTemp': 'float64',
    'MonthlyMinimumTemp': 'float64',
    'MonthlyMeanTemp': 'float64',
    'MonthlyAverageRH': 'float64',
    'MonthlyDewpointTemp': 'float64',
    'MonthlyWetBulbTemp': 'float64',
    'MonthlyAvgHeatingDegreeDays': 'float64',
    'MonthlyAvgCoolingDegreeDays': 'float64',
    'MonthlyStationPressure': 'float64',
    'MonthlySeaLevelPressure': 'float64',
    'MonthlyAverageWindSpeed': 'float64',
    'MonthlyDeptFromNormalMaximumTemp': 'float64',
    'MonthlyDeptFromNormalMinimumTemp': 'float64',
    'MonthlyDeptFromNormalAverageTemp': 'float64',
    'MonthlyDaysWithGT90Temp': 'float64',
    'MonthlyDaysWithLT32Temp': 'float64',
    'MonthlyDaysWithGT32Temp': 'float64',
    'MonthlyDaysWithLT0Temp': 'float64',
    'MonthlyTotalSeasonToDateHeatingDD': 'float64',
    'MonthlyTotalSeasonToDateCoolingDD': 'float64',

    # Integer
    'DAILYSunrise': 'int64',
    'DAILYSunset': 'int64',
    'MonthlyMaxSeaLevelPressureDate': 'int64',
    'MonthlyMaxSeaLevelPressureTime': 'int64',
    'MonthlyMinSeaLevelPressureDate': 'int64',
    'MonthlyMinSeaLevelPressureTime': 'int64',

    # Object (string) #a changer !!!!! ______________________________________
    'STATION': 'object',
    'STATION_NAME': 'object',
    'DATE': 'object',
    'REPORTTPYE': 'object',
    'HOURLYSKYCONDITIONS': 'object',
    'HOURLYVISIBILITY': 'object',
    'HOURLYPRSENTWEATHERTYPE': 'object',
    'HOURLYDRYBULBTEMPF': 'object',
    'HOURLYDRYBULBTEMPC': 'object',
    'HOURLYWETBULBTEMPF': 'object',
    'HOURLYWETBULBTEMPC': 'object',
    'HOURLYDewPointTempF': 'object',
    'HOURLYDewPointTempC': 'object',
    'HOURLYRelativeHumidity': 'object',
    'HOURLYWindSpeed': 'object',
    'HOURLYWindDirection': 'object',
    'HOURLYStationPressure': 'object',
    'HOURLYPressureChange': 'object',
    'HOURLYSeaLevelPressure': 'object',
    'HOURLYPrecip': 'object',
    'HOURLYAltimeterSetting': 'object',
    'DAILYWeather': 'object',
    'DAILYPrecip': 'object',
    'DAILYSnowfall': 'object',
    'DAILYSnowDepth': 'object',
    'MonthlyTotalSnowfall': 'object',
    'MonthlyDeptFromNormalPrecip': 'object',
    'MonthlyTotalLiquidPrecip': 'object',
    'MonthlyGreatestSnowfall': 'object',
    'MonthlyGreatestSnowfallDate': 'object',
    'MonthlyGreatestSnowDepth': 'object',
    'MonthlyGreatestSnowDepthDate': 'object',
    'MonthlyTotalHeatingDegreeDays': 'object',
    'MonthlyTotalCoolingDegreeDays': 'object',
    'MonthlyDeptFromNormalHeatingDD': 'object',
    'MonthlyDeptFromNormalCoolingDD': 'object'
}

# Conversion des types des colonnes
for col, col_type in column_types.items():
    if col in weather_2017.columns:
        try:
            weather_2017[col] = weather_2017[col].astype(col_type)
        except ValueError:
            print(f"Erreur de conversion pour la colonne {col} vers {col_type}. Utilisation de valeurs NaN pour les valeurs non compatibles.")
            if col_type == 'float64':
                weather_2017[col] = pd.to_numeric(weather_2017[col], errors='coerce')
            elif col_type == 'int64':
                weather_2017[col] = pd.to_numeric(weather_2017[col], errors='coerce').astype('Int64')

# Afficher les types des colonnes pour vérifier
print(weather_2017.dtypes)
print(weather_2017.head())





# Extraire les colonnes qui contiennent "Monthly", "Hourly" ou "Daily"
monthly_columns = [col for col in weather_2017.columns if 'Monthly' in col]
hourly_columns = [col for col in weather_2017.columns if 'HOURLY' in col]
daily_columns = [col for col in weather_2017.columns if 'DAILY' in col]

# Convertir la colonne DATE en datetime pour faciliter la gestion des périodes
weather_2017['DATE'] = pd.to_datetime(weather_2017['DATE'])
weather_2017['YearMonth'] = weather_2017['DATE'].dt.to_period('M')  # Extraire l'année et le mois
weather_2017['YearDayHour'] = weather_2017['DATE'].dt.to_period('H')  # Extraire l'année, jour et heure
weather_2017['YearDay'] = weather_2017['DATE'].dt.to_period('D')  # Extraire l'année et jour

# Fonction pour remplir les valeurs par mois / jour / heure
def fill_periodic_values(df, columns, period_key):
    for col in columns:
        if col in df.columns:
            # Utiliser les groupes par période pour remplir les NaN avec ffill et bfill
            df[col] = df.groupby(period_key)[col].transform(lambda group: group.ffill().bfill())

fill_periodic_values(weather_2017, monthly_columns, 'YearMonth')
fill_periodic_values(weather_2017, daily_columns, 'YearDay')
fill_periodic_values(weather_2017, hourly_columns, 'YearDayHour')

# Supprimer les colonnes temporaires
weather_2017.drop(columns=['YearMonth', 'YearDayHour', 'YearDay'], inplace=True)

# Vérifier les colonnes contenant des NaN dans weather_2017
def check_nan_columns(df):
    nan_columns = df.columns[df.isna().any()].tolist()
    for col in nan_columns:
        nan_count = df[col].isna().sum()
        print(f"Colonne '{col}' contient {nan_count} valeurs NaN.")

# Appliquer la vérification
check_nan_columns(weather_2017)

#Eliminer les colonnes ou les lignes avec trop de valeurs Nan au cas par cas
# Supprimer les colonnes avec plus de 1000 valeurs NaN
weather_2017 = weather_2017.dropna(axis=1, thresh=len(weather_2017) - 1000)
print("Vérification : \n")
check_nan_columns(weather_2017)

# Afficher les premiers résultats pour validation
print(weather_2017.head())
print(len(weather_2017)) #13201

weather_2017 = weather_2017.dropna(axis=0)
check_nan_columns(weather_2017) #nothing
print(len(weather_2017)) #13027



#upload_to_s3("Pre-Processed_data", "weather_2017.csv")











# Data cleaning for the dataset of the WALS from Kaggle

# Link: https://www.kaggle.com/code/kerneler/starter-wals-dataset-ddb3fac7-a/input

import pandas as pd

# 6 steps : 
# -	Eliminate the useless columns used for language identification
# -	Eliminate the columns for non-interesting grammatical features
# -	Eliminate the languages that has not been retained
# -	Eliminate the columns for which there are too many missing values OR the languages with too many missing values (needs to count the number of missing values per row and per columns)
# -	Eliminate the columns for which there are too many similarities (needs to do a kind of exploratory statistical investigation). 
# - Make all the str values of the variable as int or float


language_df = pd.read_csv("/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/language.csv")
#print(language_df.columns)


# 1st step : Deletion of the useless columns for language identification (we only keep the Names of the languages)
# wals_code, iso_code, glottocode, macroarea, countrycodes
language_df = language_df.drop(columns=['wals_code', 'iso_code', 'glottocode', 'macroarea', 'countrycodes'])
#print(language_df.columns[0:15])


# 2nd step : Deletion of useless grammatical features (this part is the most prone to subjectivity, maybe some columns should be added afterwards)
unused_category = "4A Voicing in Plosives and Fricatives, 5A Voicing and Gaps in Plosive Systems, 6A Uvular Consonants, 7A Glottalized Consonants, 8A Lateral Consonants, 9A The Velar Nasal, 11A Front Rounded Vowels, 15A Weight-Sensitive Stress, 16A Weight Factors in Weight-Sensitive Stress Systems, 27A Reduplication, 32A Systems of Gender Assignment, 36A The Associative Plural, 40A Inclusive/Exclusive Distinction in Verbal Inflection, 42A Pronominal and Adnominal Demonstratives, 43A Third Person Pronouns and Demonstratives, 44A Gender Distinctions in Independent Personal Pronouns, 45A Politeness Distinctions in Pronouns, 46A Indefinite Pronouns, 47A Intensifiers and Reflexive Pronouns, 51A Position of Case Affixes, 54A Distributive Numerals, 56A Conjunctions and Universal Quantifiers, 57A Position of Pronominal Possessive Affixes, 58A Obligatory Possessive Inflection, 59A Possessive Classification, 61A Adjectives without Nouns, 63A Noun Phrase Conjunction, 64A Nominal and Verbal Conjunction, 69A Position of Tense-Aspect Affixes, 70A The Morphological Imperative, 71A The Prohibitive, 72A Imperative-Hortative Systems, 73A The Optative, 74A Situational Possibility, 75A Epistemic Possibility, 76A Overlap between Situational and Epistemic Modal Marking, 77A Semantic Distinctions of Evidentiality, 78A Coding of Evidentiality, 82A Order of Subject and Verb, 83A Order of Object and Verb, 85A Order of Adposition and Noun Phrase, 86A Order of Genitive and Noun, 87A Order of Adjective and Noun, 88A Order of Demonstrative and Noun, 89A Order of Numeral and Noun, 91A Order of Degree Word and Adjective, 92A Position of Polar Question Particles, 95A Relationship between the Order of Object and Verb and the Order of Adposition and Noun Phrase, 96A Relationship between the Order of Object and Verb and the Order of Relative Clause and Noun, 97A Relationship between the Order of Object and Verb and the Order of Adjective and Noun, 103A Third Person Zero of Verbal Person Marking, 104A Order of Person Markers on the Verb, 106A Reciprocal Constructions, 107A Passive Constructions, 108A Antipassive Constructions, 109A Applicative Constructions, 110A Periphrastic Causative Constructions, 111A Nonperiphrastic Causative Constructions, 112A Negative Morphemes, 113A Symmetric and Asymmetric Standard Negation, 114A Subtypes of Asymmetric Standard Negation, 115A Negative Indefinite Pronouns and Predicate Negation, 116A Polar Questions, 118A Predicative Adjectives, 119A Nominal and Locational Predication, 123A Relativization on Obliques, 125A Purpose Clauses, 126A 'When' Clauses, 127A Reason Clauses, 128A Utterance Complement Clauses, 129A Hand and Arm, 130A Finger and Hand, 131A Numeral Bases, 132A Number of Non-Derived Basic Colour Categories, 133A Number of Basic Colour Categories, 134A Green and Blue, 135A Red and Yellow, 136A M-T Pronouns, 137A N-M Pronouns, 138A Tea, 139A Irregular Negatives in Sign Languages, 140A Question Particles in Sign Languages, 142A Para-Linguistic Usages of Clicks, 143F Postverbal Negative Morphemes, 90B Prenominal relative clauses, 144Y The Position of Negative Morphemes in Object-Initial Languages, 90C Postnominal relative clauses, 144P NegSOV Order, 144J SVNegO Order, 144N Obligatory Double Negation in SOV languages, 144S SOVNeg Order, 144X Verb-Initial with Clause-Final Negative, 90G Double-headed relative clauses, 90E Correlative relative clauses, 144V Verb-Initial with Preverbal Negative, 144I SNegVO Order, 144R SONegV Order, 143B Obligatory Double Negation, 144M Multiple Negative Constructions in SOV Languages, 144U Double negation in verb-initial languages, 144G Optional Double Negation in SVO languages, 144K SVONeg Order, 144B Position of negative words relative to beginning and end of clause and with respect to adjacency to verb, 144F Obligatory Double Negation in SVO languages, 90D Internally-headed relative clauses, 144E Multiple Negative Constructions in SVO Languages, 144D The Position of Negative Morphemes in SVO Languages, 143E Preverbal Negative Morphemes, 143C Optional Double Negation, 90F Adjoined relative clauses, 143A Order of Negative Morpheme and Verb, 144W Verb-Initial with Negative that is Immediately Postverbal or between Subject and Object, 144O Optional Double Negation in SOV languages, 144Q SNegOV Order, 144L The Position of Negative Morphemes in SOV Languages, 144H NegSVO Order, 144C Languages with different word order in negative clauses, 144T The Position of Negative Morphemes in Verb-Initial Languages, 143G Minor morphological means of signaling negation, 143D Optional Triple Negation, 39B Inclusive/Exclusive Forms in Pama-Nyungan, 137B M in Second Person Singular, 136B M in First Person Singular, 109B Other Roles of Applied Objects, 10B Nasal Vowels in West Africa, 25B Zero Marking of A and P Arguments, 21B Exponence of Tense-Aspect-Mood Inflection, 108B Productivity of the Antipassive Construction, 58B Number of Possessive Nouns, 79B Suppletion in Imperatives and Hortatives, 130B Cultural Categories of Languages with Identity of 'Finger' and 'Hand', 105A Ditransitive Constructions: The Verb 'Give', 124A 'Want' Complement Subjects"
#print(unused_category.split(', '))
language_df = language_df.drop(columns=unused_category.split(', '))
#print(len(language_df.columns))
language_df = language_df.drop(columns=["84A Order of Object, Oblique, and Verb", "144A Position of Negative Word With Respect to Subject, Object, and Verb", "81B Languages with two Dominant Orders of Subject, Object, and Verb"])
#print(len(language_df.columns)) #61 columns


#3rd step: Deletion of some languages
#print(language_df['Name'])
#Only the languages used in the Programme for International Student Assessment
languages_of_interest = "Mandarin, Japanese, Korean, Estonian, Dutch, Polish, Danish, Slovene, French, Finnish, Swedish, English, Norwegian, German, Czech, Vietnamese, Latvian, Icelandic, Portuguese, Russian, Italian, Slovak, Spanish, Lithuanian, Hungarian, Belorussian, Maltese, Serbian-Croatian, Hebrew (Modern), Turkish, Ukrainian, Greek (Modern), Malay, Albanian, Bulgarian, Romanian, Kazakh, Thai, Georgian, Indonesian, Tagalog"
languages_of_interest = languages_of_interest.split(', ')
#print(len(languages_of_interest)) #41

#for i in languages_of_interest.split(', '):
    #if i not in language_df['Name'].values:
        #print(i) #all the languages were correctly spelled

language_df = language_df[language_df['Name'].isin(languages_of_interest)]
#print(language_df)

# Dealing with missing values
#Counting the missing values per column
NaN_in_columns = language_df.isna().sum().sort_values(ascending=False)
#print(NaN_in_columns[NaN_in_columns > 1])

#Beaucoup de colonnes ont des données manquantes alors qu'elles sont simples à obtenir
#solution : compléter un max de colonne par moi-même

#Counting missing values per row
NaN_in_rows = pd.DataFrame({
    'Name': language_df['Name'],
    'NaN_count' :language_df.isna().sum(axis=1)
    }).sort_values(by='NaN_count', ascending=False)
#print(NaN_in_rows[NaN_in_rows['NaN_count'] > 1])
#plus de la moitié des langues ont beaucoup de données manquantes --> il va falloir compléter par soi même

print(language_df[language_df['Name'] == 'Dutch'].T)

for i in language_df[language_df['Name'] == 'Dutch'].T.itertuples():
    print(i)

#Exporting the dataframe to complete it manually
#pip3 install openpyxl
import openpyxl
language_df.to_excel('/home/onyxia/work/Effects-Language-Diversity/Data_cleaning/languages_to_complete.xlsx')

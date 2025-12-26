import json
import os
import openpyxl
from openpyxl import Workbook

def populate_excels():
    base_path = 'data'

    # ---------------------------------------------------------
    # Hardcoded Data for Targeted States
    # ---------------------------------------------------------

    # Structure: State -> District -> List of School Dicts
    # Each school dict: 'name', 'email', 'address', 'phone'

    schools_data = {
        "Telangana": {
            "Hyderabad": [
                {"name": "Delhi Public School", "email": "admission@dpssecunderabad.in", "address": "Survey No 74, Khajaguda Village, Chitrapuri Colony Post, Hyderabad - 500104", "phone": "040 2980 6765"},
                {"name": "CHIREC International School", "email": "admissions@chirec.ac.in", "address": "Kondapur, Hyderabad", "phone": "9866461204"},
                {"name": "DDMS P. Obul Reddy Public School", "email": "info@amsporps.org", "address": "Road No. 25, Jubilee Hills, Hyderabad - 500033", "phone": "040-23548912"},
                {"name": "Bharatiya Vidya Bhavan's Public School", "email": "bvbpsjh@rediffmail.com", "address": "Road No. 71, Jubilee Hills, Hyderabad - 500096", "phone": "040-23544934"},
                {"name": "Gitanjali Senior School", "email": "info@gitanjalischools.com", "address": "Mayur Marg, Begumpet, Hyderabad - 500016", "phone": "040-27768421"},
                {"name": "St. Andrews School", "email": "contact.sas-bp@standrewsindia.com", "address": "Old Bowenpally, Secunderabad - 500011", "phone": "9550838000"},
                {"name": "St. Peter's High School", "email": "sphs.hyd@gmail.com", "address": "Plot 15-16, Saibaba Colony, Bowenpally, Secunderabad - 500011", "phone": "8555073254"},
                {"name": "St. Martin's High School", "email": "info@stmartinshighschool.in", "address": "Near BHEL R&D, Balanagar, Hyderabad - 500037", "phone": "040-23774208"},
                {"name": "Sentia The Global School", "email": "admissions@sentia.in", "address": "Beside B.K. Enclave, Road No.2, Near Miyapur Bus Depot, Hyderabad - 500049", "phone": "9985288821"},
                {"name": "Sancta Maria International School", "email": "enquiry@sanctamaria.in", "address": "Survey No. 106/107, Serilingampally, Hyderabad - 500019", "phone": "040-23011222"},
                {"name": "Akshara Vaagdevi International School", "email": "admissions@avinternationalschool.org", "address": "Bolton Road, Opp Tivoli Gardens, Secunderabad - 500003", "phone": "9573469759"},
                {"name": "Openminds Birla School", "email": "principal@dsr.edu.in", "address": "BHEL, Hyderabad", "phone": "Contact School"},
                {"name": "CMR International School", "email": "cmrinternationalschool@gmail.com", "address": "Suraram, Hyderabad", "phone": "8886777760"},
                {"name": "DAV Public School Kukatpally", "email": "princi_davkkp@yahoo.in", "address": "Vivekananda Nagar, Kukatpally", "phone": "040-23065024"},
                {"name": "Ganges Valley School", "email": "info@gangesvalleyschool.com", "address": "Nizampet Road, Hyderabad", "phone": "9666777000"},
                {"name": "Genesis School", "email": "genesisschool.kp@gmail.com", "address": "Kukatpally, Hyderabad", "phone": "7675854761"},
                {"name": "Gitanjali Devakul", "email": "office@gitanjalidevakul.com", "address": "Kukatpally, Hyderabad", "phone": "9052217292"},
                {"name": "HAL Secondary School", "email": "HALsecondaryschool@gmail.com", "address": "HAL Township, Balanagar", "phone": "040-29558582"},
                {"name": "Harvest Public School", "email": "57574@cbseshiksha.com", "address": "Khammam (Registered in Hyd Cluster)", "phone": "9248977759"},
                {"name": "Hindu Public School", "email": "hindu_pschool88@yahoo.com", "address": "Sanathnagar, Hyderabad", "phone": "9948494797"},
                {"name": "Kennedy High The Magnet School", "email": "Contact@kennedymagnet.com", "address": "Kukatpally, Hyderabad", "phone": "9705566470"},
                {"name": "Laurus The School of Excellence", "email": "info@laurustheschool.com", "address": "Nizampet Road, Hyderabad", "phone": "7702755000"},
                {"name": "Meridian School Kukatpally", "email": "principal.meridiankukatpally@gmail.com", "address": "KPHB, Hyderabad", "phone": "9912799481"},
                {"name": "Montridge School", "email": "Info@montridge.in", "address": "Gajularamaram, Hyderabad", "phone": "9550953017"},
                {"name": "Pranav International School", "email": "principalpranavschool811@gmail.com", "address": "Chintal, Hyderabad", "phone": "9441200508"},
                {"name": "Quantum Leap School", "email": "admin@quantumleapschool.in", "address": "Hafeezpet, Hyderabad", "phone": "9000103540"},
                {"name": "Radcliffe School", "email": "hyderabadschool@radcliffe.in", "address": "Balanagar, Hyderabad", "phone": "9963400188"},
                {"name": "Rainbow High School", "email": "5772@cbseshiksa.in", "address": "Chintal, Hyderabad", "phone": "7794926474"},
                {"name": "Rajadhani Residential School", "email": "info2rajadhani@gmail.com", "address": "Nizampet, Hyderabad", "phone": "7702577170"},
                {"name": "Shikhara School", "email": "shikharaschool2022@gmail.com", "address": "Bowrampet, Hyderabad", "phone": "8096750007"},
                {"name": "Sri Ram School", "email": "srscbse@gmail.com", "address": "Nizampet, Hyderabad", "phone": "9985850111"},
                {"name": "Sri Sloka School", "email": "SRISLOKASCHOOL@GMAIL.COM", "address": "Gandimaisamma, Hyderabad", "phone": "9885780235"},
                {"name": "Tatva Global School", "email": "info@tatvaglobalschool.com", "address": "Gajularamaram, Hyderabad", "phone": "040-48588661"},
                {"name": "The Creek Planet School (Mercury)", "email": "info.mercury@thecreekschool.com", "address": "Bowrampet, Hyderabad", "phone": "9704882274"},
                {"name": "The Creek Planet School (Neptune)", "email": "info.neptune@thecreekschool.com", "address": "Kukatpally, Hyderabad", "phone": "8583061969"},
                {"name": "Unicent School", "email": "neelima.k@unicentbachupally.in", "address": "Bowrampet, Hyderabad", "phone": "9160003825"},
                {"name": "Vignan Vidyalaya", "email": "57620@cbseshiksha.in", "address": "Nizampet, Hyderabad", "phone": "8179554172"},
                {"name": "Vijetha Vidyalaya", "email": "vijethavidyalaya21@gmail.com", "address": "P.R. Nagar, Hyderabad", "phone": "9866660521"}
            ],
            "Warangal (Urban)": [
                {"name": "Lotus National School", "email": "lotuswarangalhoc@lotusschool.in", "address": "Opp: Koti Cheruvu, Gowthami Nagar, Warangal - 506011", "phone": "92480 24494"},
                {"name": "St. Peter's Edu School", "email": "info@stpeterseduschool.com", "address": "Hanamkonda, Warangal", "phone": "Contact School"}
            ]
        },
        "Andhra Pradesh": {
            "Visakhapatnam": [
                {"name": "Adarsh Public School", "email": "mahamadhav69@gmail.com", "address": "Vinayak Nagar, Pedagantyuda, Visakhapatnam", "phone": "0891 2511251"},
                {"name": "Alluri Sitaramaraju Pub.School", "email": "pvsnr.varma03@gmail.com", "address": "Arakku Valley, Visakhapatnam", "phone": "8936 249648"},
                {"name": "Ameya World School", "email": "principal@ameyaworldschool.in", "address": "Sangivalasa, Visakhapatnam", "phone": "Contact School"},
                {"name": "Apple I English Medium School", "email": "principal.appleiemschool@gmail.com", "address": "Gajuwaka, Visakhapatnam", "phone": "Contact School"},
                {"name": "Bal Bharati Public School", "email": "mpadmajamurthy@yahoo.in", "address": "NTPC Township, Visakhapatnam", "phone": "Contact School"},
                {"name": "D A V Centenary Public School", "email": "davukku@gmail.com", "address": "Sector-III Ukkunagaram, Visakhapatnam", "phone": "Contact School"},
                {"name": "D.A.V. Public School", "email": "davsnvsp@yahoo.com", "address": "Sujathanagar, Visakhapatnam", "phone": "Contact School"},
                {"name": "Da Vinci International School", "email": "57186@cbseshiksha.in", "address": "Thimmarajupeta, Visakhapatnam", "phone": "Contact School"},
                {"name": "Delhi Public School (Ukkunagaram)", "email": "dpsvisakhapatnam@gmail.com", "address": "Sector-VIII Ukkunagaram, Visakhapatnam", "phone": "Contact School"},
                {"name": "Delhi Public School (Anandapuram)", "email": "info@dpsvizag.org", "address": "Anandapuram, Visakhapatnam", "phone": "Contact School"},
                {"name": "Dr.Kkrs Gowtham School", "email": "gambeeramschool@gmail.com", "address": "Gambeeram Village, Visakhapatnam", "phone": "Contact School"},
                {"name": "Ekalavya Model Residential School", "email": "garvinwaters@gmail.com", "address": "Araku Valley, Visakhapatnam", "phone": "Contact School"},
                {"name": "Green City English Medium School", "email": "vs.englishaccent@gmail.com", "address": "Green City, Vadlapudi, Visakhapatnam", "phone": "Contact School"},
                {"name": "Greendale School", "email": "greendale2014@gmail.com", "address": "Madhurawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Jawahar Navodaya Vidyalaya", "email": "s.kudipudi0@gmail.com", "address": "Kommadi, Visakhapatnam", "phone": "Contact School"},
                {"name": "Kakatiya Public School", "email": "nsrinivash22@gmail.com", "address": "B C Road, Visakhapatnam", "phone": "Contact School"},
                {"name": "Kendriya Vidyalaya (Steel Plant)", "email": "srinivasulugubbala@gmail.com", "address": "Visakhapatnam Steel Plant", "phone": "Contact School"},
                {"name": "Little Angels School", "email": "littleangels.ukku.vsp@gmail.com", "address": "Sector 9 Ukkunagram, Visakhapatnam", "phone": "Contact School"},
                {"name": "Little Angles School (MVP)", "email": "littleangelschoolsvizag@yahoo.co.in", "address": "MVP Colony, Visakhapatnam", "phone": "Contact School"},
                {"name": "M.P. & E.V. School", "email": "murali6768@yahoo.co.in", "address": "Sheela Nagar, Visakhapatnam", "phone": "Contact School"},
                {"name": "Narayana English Medium School", "email": "venugopalsrk@narayanagroup.com", "address": "Paradesipalem, Visakhapatnam", "phone": "Contact School"},
                {"name": "Navy Children School", "email": "ncs_visakha@rediffmail.com", "address": "Nausena Baugh, Visakhapatnam", "phone": "Contact School"},
                {"name": "Oakridge International School", "email": "arupkumar.ray@oakridge.in", "address": "Tagarapuvalasa, Visakhapatnam", "phone": "Contact School"},
                {"name": "Om Sai English Medium School", "email": "omsaicbseschool@gmail.com", "address": "Ananthavaram, Visakhapatnam", "phone": "Contact School"},
                {"name": "Pollocks Intelli School", "email": "cbse@intellischool.in", "address": "Madhurawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Ramanath Secondary School", "email": "ramanath_school@yahoo.com", "address": "NSTL Nagar, Visakhapatnam", "phone": "Contact School"},
                {"name": "Rishi Vidyalaya", "email": "rvgsrinivas@gmail.com", "address": "Visakhapatnam", "phone": "Contact School"},
                {"name": "S R Digi School", "email": "vizag@srdigischool.com", "address": "Zinc Smelter Post, Visakhapatnam", "phone": "0891-2747070"},
                {"name": "Sanskruti Global School", "email": "sgscbse@gmail.com", "address": "Parawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "SFS School", "email": "sfsschoolcbsevizag@gmail.com", "address": "Seethammadhara, Visakhapatnam", "phone": "Contact School"},
                {"name": "Silver Oaks", "email": "principal@vizag.silveroaks.co.in", "address": "Rushikonda, Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Chaitanya Techno School", "email": "pardhuson@gmail.com", "address": "Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Chaitanya Vidya Niketan", "email": "knr279@gmail.com", "address": "Madhurawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Prakash Vidya Niketan", "email": "sriprakashcbse.kplpd@gmail.com", "address": "Kapuluppada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Prakash Vidyaniketan", "email": "info@sriprakashschools.com", "address": "Uplands, Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Sathya Sai Vidya Vihar", "email": "kausalya.ayyagari@gmail.com", "address": "MVP Colony, Visakhapatnam", "phone": "Contact School"},
                {"name": "Sri Tvs Rao Srikrishna Vidya Mandir", "email": "raopj1957@gmail.com", "address": "Dwaraka Nagar, Visakhapatnam", "phone": "Contact School"},
                {"name": "Srishti World School", "email": "srishtiworldschool@gmail.com", "address": "Ukkunagaram, Visakhapatnam", "phone": "Contact School"},
                {"name": "St. John's School", "email": "principal@stjohnscbse.co.in", "address": "Kasimkota, Visakhapatnam", "phone": "Contact School"},
                {"name": "St.Anns School", "email": "stanns.schoolcsavsp2011@gmail.com", "address": "Madhurawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "SVVP High School", "email": "svvpschoolgpm@gmail.com", "address": "Gopalapatnam, Visakhapatnam", "phone": "Contact School"},
                {"name": "The Presidential School", "email": "presidentialschool@rediffmail.com", "address": "Bheemunipatnam, Visakhapatnam", "phone": "Contact School"},
                {"name": "Timpany Secondary School", "email": "vandanaanandabraham@gmail.com", "address": "Visakhapatnam", "phone": "Contact School"},
                {"name": "Timpany Steel City School", "email": "rezeenavkumar@gmail.com", "address": "Pedagantyada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Vignan Steel City Public School", "email": "madhu4hari@gmail.com", "address": "Duvvada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Vignan Vidyalayam School", "email": "principal.vignanschool@gmail.com", "address": "Thimmapuram, Visakhapatnam", "phone": "Contact School"},
                {"name": "Vijayam School", "email": "vijayamschoolmadhurawada@gmail.com", "address": "Madhurawada, Visakhapatnam", "phone": "Contact School"},
                {"name": "Vijnana Vihara Residential School", "email": "rgantik@yahoo.com", "address": "Gudilova, Visakhapatnam", "phone": "Contact School"},
                {"name": "Vikas Vidyaniketan", "email": "chsrao@vikasonline.com", "address": "Sheela Nagar, Visakhapatnam", "phone": "Contact School"},
                {"name": "Visakha Valley School", "email": "nath_nv@yahoo.com", "address": "China Gadili, Visakhapatnam", "phone": "Contact School"},
                {"name": "Visvodaya School", "email": "visvodayaednsociety@gmail.com", "address": "Kancharapalem, Visakhapatnam", "phone": "Contact School"}
            ]
        },
        "Bihar": {
            "Patna": [
                {"name": "St. Michael's High School", "email": "michaelpatna@gmail.com", "address": "Digha Ghat, Patna - 800011", "phone": "0612-2567450"},
                {"name": "Notre Dame Academy", "email": "info.ndapatna@gmail.com", "address": "Patliputra Colony, Patna - 800013", "phone": "0612-2262332"},
                {"name": "Loyola High School", "email": "loyolapat@yahoo.com", "address": "Kurji, Patna - 800010", "phone": "0612-2262272"},
                {"name": "St. Karen's High School", "email": "contact@stkarenshighschool.com", "address": "Gola Road, Danapur, Patna - 801503", "phone": "+91 754 181 2077"},
                {"name": "Delhi Public School Patna", "email": "info@dpspatna.com", "address": "Vill. Chandmari, Danapur, Patna - 801502", "phone": "9973311118"},
                {"name": "Gyan Niketan Girls School", "email": "gyanniketangirlsschool@rediffmail.com", "address": "Rukmini Vihar, Ashiana Digha Road, Patna - 800011", "phone": "9263636382"},
                {"name": "Krishna Niketan Girls School", "email": "krishnaniketangirlsschool2@gmail.com", "address": "Darshan Vihar, Patna - 800006", "phone": "8409283270"},
                {"name": "St. Xavier's High School", "email": "contact@stxavierspatna.in", "address": "West Gandhi Maidan, Patna - 800001", "phone": "0612-2219563"},
                {"name": "Manava Bharati India International School", "email": "admin@mbispatna.org", "address": "Near AIIMS Patna, Phulwari Sharif, Patna", "phone": "8102450507"},
                {"name": "Kendriya Vidyalaya Kankarbagh", "email": "kvsropatna@yahoo.com", "address": "Lohiya Nagar, Kankarbagh, Patna", "phone": "0612-2361701"},
                {"name": "Kendriya Vidyalaya Bailey Road", "email": "ppl.baileyroad@kvs.gov.in", "address": "Bailey Road, Patna", "phone": "Contact School"},
                {"name": "Kendriya Vidyalaya Danapur Cantt", "email": "ppl.danapurcantt@kvs.gov.in", "address": "Danapur Cantt, Patna", "phone": "Contact School"},
                {"name": "St. Karen's Secondary School", "email": "contact@stkarenssecondaryschool.com", "address": "Khagaul Road, Patna", "phone": "Contact School"},
                {"name": "St. Karen's Collegiate School", "email": "contact@stkarenscollegiateschool.com", "address": "Bihta, Patna", "phone": "Contact School"},
                {"name": "Radiant International School", "email": "contact@radiantpatna.com", "address": "Khagaul Road, Patna", "phone": "Contact School"}
            ],
            "Katihar": [
                {"name": "Kendriya Vidyalaya Katihar", "email": "kvkatihar@gmail.com", "address": "Langra Bagan, Sahebpara, Katihar - 854105", "phone": "06452-231397"}
            ],
            "Muzaffarpur": [
                {"name": "Kendriya Vidyalaya CRPF Jhaphan", "email": "ppl.jhaphancrpf@kvs.gov.in", "address": "Group Centre CRPF, Jhaphan, Muzaffarpur", "phone": "0621-2814356"}
            ],
            "Darbhanga": [
                {"name": "Kendriya Vidyalaya No. 2", "email": "ppl.darbhangano2iti@kvs.gov.in", "address": "Air Force Station, Darbhanga", "phone": "06272-225038"}
            ]
        },
        "Jharkhand": {
            "Ranchi": [
                {"name": "Delhi Public School Ranchi", "email": "info@dpsranchi.com", "address": "Sail Township, Dhurwa, Ranchi - 834004", "phone": "0651 244 1176"},
                {"name": "Surendranath Centenary School", "email": "surendranathranchi@gmail.com", "address": "H.B. Road, Dipatoli, Ranchi - 834009", "phone": "9430113676"},
                {"name": "Cambrian Public School", "email": "info@cambrianpublicschool.com", "address": "Kanke Road, Ranchi - 834008", "phone": "0651-3510010"},
                {"name": "Bishop Westcott Boys' School", "email": "bwbs_namkum@yahoo.co.in", "address": "Namkum, Ranchi - 834010", "phone": "0651-6565004"},
                {"name": "St. Xavier's College (Inter)", "email": "info@sxcran.org", "address": "Dr. Camil Bulcke Path, Ranchi - 834001", "phone": "0651 2214301"},
                {"name": "Lady K C Roy Memorial School", "email": "info@lkcrms.edu.in", "address": "Ranchi, Jharkhand", "phone": "Contact School"}
            ],
            "East Singhbhum": [
                {"name": "D.B.M.S Kadma High School", "email": "dbmskhs@dbmskhs.org", "address": "Road no. 23, Farm Area, Kadma, Jamshedpur - 831005", "phone": "0657-2309192"},
                {"name": "DAV Public School Bistupur", "email": "dav.bistupur@gmail.com", "address": "Contractors' Area, Road No 4, Bistupur, Jamshedpur", "phone": "0657-2226745"},
                {"name": "Delhi Public School Jamshedpur", "email": "dpsjsr.in@gmail.com", "address": "Village Turiabera, Mango, Jamshedpur", "phone": "9472729746"},
                {"name": "Hill Top School", "email": "contact@hilltopschooljamshedpur.org", "address": "Telco Colony, Jamshedpur", "phone": "0657-2286677"},
                {"name": "Kerala Public School Kadma", "email": "kpschairman@yahoo.in", "address": "Uliyan, Kadma, Jamshedpur", "phone": "7280008955"},
                {"name": "St. Mary's High School", "email": "smehsbjsr@gmail.com", "address": "Kharkai Link Road, Bistupur, Jamshedpur", "phone": "0657-2320078"},
                {"name": "Jamshedpur Public School", "email": "jpsaiwc1988@gmail.com", "address": "Panchvati Road, New Baridih, Jamshedpur", "phone": "0657-2344050"},
                {"name": "Kendriya Vidyalaya Tatanagar", "email": "ppl.tatanagar@kvs.gov.in", "address": "Railway Engg Colony, Tatanagar, Jamshedpur", "phone": "8210086712"},
                {"name": "Sacred Heart Convent School", "email": "jsrshs@gmail.com", "address": "Park Road, Northern Town, Bistupur, Jamshedpur", "phone": "0657 2431478"}
            ],
            "Dhanbad": [
                {"name": "Sahodaya School Complex", "email": "info@sahodayadhanbad.com", "address": "DAV Public School, Koyalanagar, Dhanbad", "phone": "+91 9431392666"}
            ],
            "Garhwa": [
                {"name": "Kendriya Vidyalaya Garhwa", "email": "ppl.garhwa@kvs.gov.in", "address": "Pipra Kalan, Gayatri Nagar, Garhwa", "phone": "9458165703"}
            ],
            "Godda": [
                {"name": "Kendriya Vidyalaya Godda", "email": "ppl.godda@kvs.gov.in", "address": "Godda, Jharkhand", "phone": "8134956371"}
            ],
            "Jamtara": [
                {"name": "Kendriya Vidyalaya Jamtara", "email": "ppl.jamtara@kvs.gov.in", "address": "Dakshin Bahal, Jamtara", "phone": "8617307793"}
            ],
            "Latehar": [
                {"name": "Kendriya Vidyalaya Latehar", "email": "ppl.latehar@kvs.gov.in", "address": "Latehar, Jharkhand", "phone": "9453369555"}
            ],
            "Deoghar": [
                {"name": "Kendriya Vidyalaya Madhupur", "email": "ppl.madhupur@kvs.gov.in", "address": "Near Polytechnic College, Madhupur, Deoghar", "phone": "Contact School"}
            ]
        }
    }

    # Helper to clean directory names
    def clean_name(n):
        return n.strip().replace('/', '_')

    total_schools = 0

    # Iterate and create Excel files
    for state, districts in schools_data.items():
        state_dir = os.path.join(base_path, clean_name(state))

        for district, schools in districts.items():
            district_dir = os.path.join(state_dir, clean_name(district))

            # Create district folder if it doesn't exist (it should, but safety first)
            os.makedirs(district_dir, exist_ok=True)

            excel_path = os.path.join(district_dir, f"{clean_name(district)}_Schools.xlsx")

            wb = Workbook()
            ws = wb.active
            ws.title = "Schools"

            # Headers
            headers = ["School Name", "Email ID", "Address", "Contact Number"]
            ws.append(headers)

            for school in schools:
                ws.append([
                    school.get('name', ''),
                    school.get('email', ''),
                    school.get('address', ''),
                    school.get('phone', '')
                ])
                total_schools += 1

            wb.save(excel_path)
            print(f"Generated: {excel_path} with {len(schools)} schools.")

    print(f"Total verified schools added: {total_schools}")

if __name__ == "__main__":
    populate_excels()

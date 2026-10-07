export interface StateCountyData {
  code: string;
  name: string;
  region: "Northeast" | "Midwest" | "South" | "West" | "Territories";
  capital: string;
  sampleCity: string;
  sampleZip: string;
  fipsPrefix: string;
  totalCountiesCount: number;
  counties: string[];
}

export const ALL_50_STATES: StateCountyData[] = [
  {
    code: "AL",
    name: "Alabama",
    region: "South",
    capital: "Montgomery",
    sampleCity: "Birmingham",
    sampleZip: "35203",
    fipsPrefix: "01",
    totalCountiesCount: 67,
    counties: [
      "Autauga", "Baldwin", "Barbour", "Bibb", "Blount", "Bullock", "Butler", "Calhoun", "Chambers", "Cherokee",
      "Chilton", "Choctaw", "Clarke", "Clay", "Cleburne", "Coffee", "Colbert", "Conecuh", "Coosa", "Covington",
      "Crenshaw", "Cullman", "Dale", "Dallas", "DeKalb", "Elmore", "Escambia", "Etowah", "Fayette", "Franklin",
      "Geneva", "Greene", "Hale", "Henry", "Houston", "Jackson", "Jefferson", "Lamar", "Lauderdale", "Lawrence",
      "Lee", "Limestone", "Lowndes", "Macon", "Madison", "Marengo", "Marion", "Marshall", "Mobile", "Monroe",
      "Montgomery", "Morgan", "Perry", "Pickens", "Pike", "Randolph", "Russell", "St. Clair", "Shelby", "Sumter",
      "Talladega", "Tallapoosa", "Tuscaloosa", "Walker", "Washington", "Wilcox", "Winston"
    ]
  },
  {
    code: "AK",
    name: "Alaska",
    region: "West",
    capital: "Juneau",
    sampleCity: "Anchorage",
    sampleZip: "99501",
    fipsPrefix: "02",
    totalCountiesCount: 29,
    counties: [
      "Aleutians East", "Aleutians West", "Anchorage", "Bethel", "Bristol Bay", "Denali", "Dillingham",
      "Fairbanks North Star", "Haines", "Hoonah-Angoon", "Juneau", "Kenai Peninsula", "Ketchikan Gateway",
      "Kodiak Island", "Kusilvak", "Lake and Peninsula", "Matanuska-Susitna", "Nome", "North Slope",
      "Northwest Arctic", "Petersburg", "Prince of Wales-Hyder", "Sitka", "Skagway", "Southeast Fairbanks",
      "Valdez-Cordova", "Wrangell", "Yakutat", "Yukon-Koyukuk"
    ]
  },
  {
    code: "AZ",
    name: "Arizona",
    region: "West",
    capital: "Phoenix",
    sampleCity: "Phoenix",
    sampleZip: "85001",
    fipsPrefix: "04",
    totalCountiesCount: 15,
    counties: [
      "Apache", "Cochise", "Coconino", "Gila", "Graham", "Greenlee", "La Paz", "Maricopa", "Mohave", "Navajo",
      "Pima", "Pinal", "Santa Cruz", "Yavapai", "Yuma"
    ]
  },
  {
    code: "AR",
    name: "Arkansas",
    region: "South",
    capital: "Little Rock",
    sampleCity: "Little Rock",
    sampleZip: "72201",
    fipsPrefix: "05",
    totalCountiesCount: 75,
    counties: [
      "Arkansas", "Ashley", "Baxter", "Benton", "Boone", "Bradley", "Calhoun", "Carroll", "Chicot", "Clark",
      "Clay", "Cleburne", "Cleveland", "Columbia", "Conway", "Craighead", "Crawford", "Crittenden", "Cross", "Dallas",
      "Desha", "Drew", "Faulkner", "Franklin", "Fulton", "Garland", "Grant", "Greene", "Hempstead", "Hot Spring",
      "Howard", "Independence", "Izard", "Jackson", "Jefferson", "Johnson", "Lafayette", "Lawrence", "Lee", "Lincoln",
      "Little River", "Logan", "Lonoke", "Madison", "Marion", "Miller", "Mississippi", "Monroe", "Montgomery", "Nevada",
      "Newton", "Ouachita", "Perry", "Phillips", "Pike", "Poinsett", "Polk", "Pope", "Prairie", "Pulaski",
      "Randolph", "St. Francis", "Saline", "Scott", "Searcy", "Sebastian", "Sevier", "Sharp", "Stone", "Union",
      "Van Buren", "Washington", "White", "Woodruff", "Yell"
    ]
  },
  {
    code: "CA",
    name: "California",
    region: "West",
    capital: "Sacramento",
    sampleCity: "Los Angeles",
    sampleZip: "90012",
    fipsPrefix: "06",
    totalCountiesCount: 58,
    counties: [
      "Alameda", "Alpine", "Amador", "Butte", "Calaveras", "Colusa", "Contra Costa", "Del Norte", "El Dorado", "Fresno",
      "Glenn", "Humboldt", "Imperial", "Inyo", "Kern", "Kings", "Lake", "Lassen", "Los Angeles", "Madera",
      "Marin", "Mariposa", "Mendocino", "Merced", "Modoc", "Mono", "Monterey", "Napa", "Nevada", "Orange",
      "Placer", "Plumas", "Riverside", "Sacramento", "San Benito", "San Bernardino", "San Diego", "San Francisco", "San Joaquin", "San Luis Obispo",
      "San Mateo", "Santa Barbara", "Santa Clara", "Santa Cruz", "Shasta", "Sierra", "Siskiyou", "Solano", "Sonoma", "Stanislaus",
      "Sutter", "Tehama", "Trinity", "Tulare", "Tuolumne", "Ventura", "Yolo", "Yuba"
    ]
  },
  {
    code: "CO",
    name: "Colorado",
    region: "West",
    capital: "Denver",
    sampleCity: "Denver",
    sampleZip: "80202",
    fipsPrefix: "08",
    totalCountiesCount: 64,
    counties: [
      "Adams", "Alamosa", "Arapahoe", "Archuleta", "Baca", "Bent", "Boulder", "Broomfield", "Chaffee", "Cheyenne",
      "Clear Creek", "Conejos", "Costilla", "Crowley", "Custer", "Delta", "Denver", "Dolores", "Douglas", "Eagle",
      "Elbert", "El Paso", "Fremont", "Garfield", "Gilpin", "Grand", "Gunnison", "Hinsdale", "Huerfano", "Jackson",
      "Jefferson", "Kiowa", "Kit Carson", "Lake", "La Plata", "Larimer", "Las Animas", "Lincoln", "Logan", "Mesa",
      "Mineral", "Moffat", "Montezuma", "Montrose", "Morgan", "Otero", "Ouray", "Park", "Phillips", "Pitkin",
      "Prowers", "Pueblo", "Rio Blanco", "Rio Grande", "Routt", "Saguache", "San Juan", "San Miguel", "Sedgwick", "Summit",
      "Teller", "Washington", "Weld", "Yuma"
    ]
  },
  {
    code: "CT",
    name: "Connecticut",
    region: "Northeast",
    capital: "Hartford",
    sampleCity: "Hartford",
    sampleZip: "06103",
    fipsPrefix: "09",
    totalCountiesCount: 8,
    counties: [
      "Fairfield", "Hartford", "Litchfield", "Middlesex", "New Haven", "New London", "Tolland", "Windham"
    ]
  },
  {
    code: "DE",
    name: "Delaware",
    region: "South",
    capital: "Dover",
    sampleCity: "Wilmington",
    sampleZip: "19801",
    fipsPrefix: "10",
    totalCountiesCount: 3,
    counties: [
      "Kent", "New Castle", "Sussex"
    ]
  },
  {
    code: "DC",
    name: "District of Columbia",
    region: "South",
    capital: "Washington",
    sampleCity: "Washington",
    sampleZip: "20001",
    fipsPrefix: "11",
    totalCountiesCount: 1,
    counties: [
      "District of Columbia"
    ]
  },
  {
    code: "FL",
    name: "Florida",
    region: "South",
    capital: "Tallahassee",
    sampleCity: "Lawtey",
    sampleZip: "32058",
    fipsPrefix: "12",
    totalCountiesCount: 67,
    counties: [
      "Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward", "Calhoun", "Charlotte", "Citrus", "Clay",
      "Collier", "Columbia", "DeSoto", "Dixie", "Duval", "Escambia", "Flagler", "Franklin", "Gadsden", "Gilchrist",
      "Glades", "Gulf", "Hamilton", "Hardee", "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes", "Indian River",
      "Jackson", "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy", "Liberty", "Madison", "Manatee",
      "Marion", "Martin", "Miami-Dade", "Monroe", "Nassau", "Okaloosa", "Okeechobee", "Orange", "Osceola", "Palm Beach",
      "Pasco", "Pinellas", "Polk", "Putnam", "St. Johns", "St. Lucie", "Santa Rosa", "Sarasota", "Seminole", "Sumter",
      "Suwannee", "Taylor", "Union", "Volusia", "Wakulla", "Walton", "Washington"
    ]
  },
  {
    code: "GA",
    name: "Georgia",
    region: "South",
    capital: "Atlanta",
    sampleCity: "Atlanta",
    sampleZip: "30303",
    fipsPrefix: "13",
    totalCountiesCount: 159,
    counties: [
      "Appling", "Atkinson", "Bacon", "Baker", "Baldwin", "Banks", "Barrow", "Bartow", "Ben Hill", "Berrien",
      "Bibb", "Bleckley", "Brantley", "Brooks", "Bryan", "Bulloch", "Burke", "Butts", "Calhoun", "Camden",
      "Candler", "Carroll", "Catoosa", "Charlton", "Chatham", "Chattahoochee", "Chattooga", "Cherokee", "Clarke", "Clay",
      "Clayton", "Clinch", "Cobb", "Coffee", "Colquitt", "Columbia", "Cook", "Coweta", "Crawford", "Crisp",
      "Dade", "Dawson", "Decatur", "DeKalb", "Dodge", "Dooly", "Dougherty", "Douglas", "Early", "Echols",
      "Effingham", "Elbert", "Emanuel", "Evans", "Fannin", "Fayette", "Floyd", "Forsyth", "Franklin", "Fulton",
      "Gilmer", "Glascock", "Glynn", "Gordon", "Grady", "Greene", "Gwinnett", "Habersham", "Hall", "Hancock",
      "Haralson", "Harris", "Hart", "Heard", "Henry", "Houston", "Irwin", "Jackson", "Jasper", "Jeff Davis",
      "Jefferson", "Jenkins", "Johnson", "Jones", "Lamar", "Lanier", "Laurens", "Lee", "Liberty", "Lincoln",
      "Long", "Lowndes", "Lumpkin", "McDuffie", "McIntosh", "Macon", "Madison", "Marion", "Meriwether", "Miller",
      "Milton", "Mitchell", "Monroe", "Montgomery", "Morgan", "Murray", "Muscogee", "Newton", "Oconee", "Oglethorpe",
      "Paulding", "Peach", "Pickens", "Pierce", "Pike", "Polk", "Pulaski", "Putnam", "Quitman", "Rabun",
      "Randolph", "Richmond", "Rockdale", "Schley", "Screven", "Seminole", "Spalding", "Stephens", "Stewart", "Sumter",
      "Talbot", "Taliaferro", "Tattnall", "Taylor", "Telfair", "Terrell", "Thomas", "Tift", "Toombs", "Towns",
      "Treutlen", "Troup", "Turner", "Twiggs", "Union", "Upson", "Walker", "Walton", "Ware", "Warren",
      "Washington", "Wayne", "Webster", "Wheeler", "White", "Whitfield", "Wilcox", "Wilkes", "Wilkinson", "Worth"
    ]
  },
  {
    code: "HI",
    name: "Hawaii",
    region: "West",
    capital: "Honolulu",
    sampleCity: "Honolulu",
    sampleZip: "96813",
    fipsPrefix: "15",
    totalCountiesCount: 5,
    counties: [
      "Hawaii", "Honolulu", "Kalawao", "Kauai", "Maui"
    ]
  },
  {
    code: "ID",
    name: "Idaho",
    region: "West",
    capital: "Boise",
    sampleCity: "Boise",
    sampleZip: "83702",
    fipsPrefix: "16",
    totalCountiesCount: 44,
    counties: [
      "Ada", "Adams", "Bannock", "Bear Lake", "Benewah", "Bingham", "Blaine", "Boise", "Bonner", "Bonneville",
      "Boundary", "Butte", "Camas", "Canyon", "Caribou", "Cassia", "Clark", "Clearwater", "Custer", "Elmore",
      "Franklin", "Fremont", "Gem", "Gooding", "Idaho", "Jefferson", "Jerome", "Kootenai", "Latah", "Lemhi",
      "Lewis", "Lincoln", "Madison", "Minidoka", "Nez Perce", "Oneida", "Owyhee", "Payette", "Power", "Shoshone",
      "Teton", "Twin Falls", "Valley", "Washington"
    ]
  },
  {
    code: "IL",
    name: "Illinois",
    region: "Midwest",
    capital: "Springfield",
    sampleCity: "Chicago",
    sampleZip: "60601",
    fipsPrefix: "17",
    totalCountiesCount: 102,
    counties: [
      "Adams", "Alexander", "Bond", "Boone", "Brown", "Bureau", "Calhoun", "Carroll", "Cass", "Champaign",
      "Christian", "Clark", "Clay", "Clinton", "Coles", "Cook", "Crawford", "Cumberland", "DeKalb", "DeWitt",
      "Douglas", "DuPage", "Edgar", "Edwards", "Effingham", "Fayette", "Ford", "Franklin", "Fulton", "Gallatin",
      "Greene", "Grundy", "Hamilton", "Hancock", "Hardin", "Henderson", "Henry", "Iroquois", "Jackson", "Jasper",
      "Jefferson", "Jersey", "Jo Daviess", "Johnson", "Kane", "Kankakee", "Kendall", "Knox", "Lake", "LaSalle",
      "Lawrence", "Lee", "Livingston", "Logan", "McDonough", "McHenry", "McLean", "Macon", "Macoupin", "Madison",
      "Marion", "Marshall", "Mason", "Massac", "Menard", "Mercer", "Monroe", "Montgomery", "Morgan", "Moultrie",
      "Ogle", "Peoria", "Perry", "Piatt", "Pike", "Pope", "Pulaski", "Putnam", "Randolph", "Richland",
      "Rock Island", "St. Clair", "Saline", "Sangamon", "Schuyler", "Scott", "Shelby", "Stark", "Stephenson", "Tazewell",
      "Union", "Vermilion", "Wabash", "Warren", "Washington", "Wayne", "White", "Whiteside", "Will", "Williamson",
      "Winnebago", "Woodford"
    ]
  },
  {
    code: "IN",
    name: "Indiana",
    region: "Midwest",
    capital: "Indianapolis",
    sampleCity: "Indianapolis",
    sampleZip: "46204",
    fipsPrefix: "18",
    totalCountiesCount: 92,
    counties: [
      "Adams", "Allen", "Bartholomew", "Benton", "Blackford", "Boone", "Brown", "Carroll", "Cass", "Clark",
      "Clay", "Clinton", "Crawford", "Daviess", "Dearborn", "Decatur", "DeKalb", "Delaware", "Dubois", "Elkhart",
      "Fayette", "Floyd", "Fountain", "Franklin", "Fulton", "Gibson", "Grant", "Greene", "Hamilton", "Hancock",
      "Harrison", "Hendricks", "Henry", "Howard", "Huntington", "Jackson", "Jasper", "Jay", "Jefferson", "Jennings",
      "Johnson", "Knox", "Kosciusko", "LaGrange", "Lake", "LaPorte", "Lawrence", "Madison", "Marion", "Marshall",
      "Martin", "Miami", "Monroe", "Montgomery", "Morgan", "Newton", "Noble", "Ohio", "Orange", "Owen",
      "Parke", "Perry", "Pike", "Porter", "Posey", "Pulaski", "Putnam", "Randolph", "Ripley", "Rush",
      "St. Joseph", "Scott", "Shelby", "Spencer", "Starke", "Steuben", "Sullivan", "Switzerland", "Tippecanoe", "Tipton",
      "Union", "Vanderburgh", "Vermillion", "Vigo", "Wabash", "Warren", "Warrick", "Washington", "Wayne", "Wells",
      "White", "Whitley"
    ]
  },
  {
    code: "IA",
    name: "Iowa",
    region: "Midwest",
    capital: "Des Moines",
    sampleCity: "Des Moines",
    sampleZip: "50309",
    fipsPrefix: "19",
    totalCountiesCount: 99,
    counties: [
      "Adair", "Adams", "Allamakee", "Appanoose", "Audubon", "Benton", "Black Hawk", "Boone", "Bremer", "Buchanan",
      "Buena Vista", "Butler", "Calhoun", "Carroll", "Cass", "Cedar", "Cerro Gordo", "Cherokee", "Chickasaw", "Clarke",
      "Clay", "Clayton", "Clinton", "Crawford", "Dallas", "Davis", "Decatur", "Delaware", "Des Moines", "Dickinson",
      "Dubuque", "Emmet", "Fayette", "Floyd", "Franklin", "Fremont", "Greene", "Grundy", "Guthrie", "Hamilton",
      "Hancock", "Hardin", "Harrison", "Henry", "Howard", "Humboldt", "Ida", "Iowa", "Jackson", "Jasper",
      "Jefferson", "Johnson", "Jones", "Keokuk", "Kossuth", "Lee", "Linn", "Louisa", "Lucas", "Lyon",
      "Madison", "Mahaska", "Marion", "Marshall", "Mills", "Mitchell", "Monona", "Monroe", "Montgomery", "Muscatine",
      "O'Brien", "Osceola", "Page", "Palo Alto", "Plymouth", "Pocahontas", "Polk", "Pottawattamie", "Poweshiek", "Ringgold",
      "Sac", "Scott", "Shelby", "Sioux", "Story", "Tama", "Taylor", "Union", "Van Buren", "Wapello",
      "Warren", "Washington", "Wayne", "Webster", "Winnebago", "Winneshiek", "Woodbury", "Worth", "Wright"
    ]
  },
  {
    code: "KS",
    name: "Kansas",
    region: "Midwest",
    capital: "Topeka",
    sampleCity: "Wichita",
    sampleZip: "67202",
    fipsPrefix: "20",
    totalCountiesCount: 105,
    counties: [
      "Allen", "Anderson", "Atchison", "Barber", "Barton", "Bourbon", "Brown", "Butler", "Chase", "Chautauqua",
      "Cherokee", "Cheyenne", "Clark", "Clay", "Cloud", "Coffey", "Comanche", "Cowley", "Crawford", "Decatur",
      "Dickinson", "Doniphan", "Douglas", "Edwards", "Elk", "Ellis", "Ellsworth", "Finney", "Ford", "Franklin",
      "Geary", "Gove", "Graham", "Grant", "Gray", "Greeley", "Greenwood", "Hamilton", "Harper", "Harvey",
      "Haskell", "Hodgeman", "Jackson", "Jefferson", "Jewell", "Johnson", "Kearny", "Kingman", "Kiowa", "Labette",
      "Lane", "Leavenworth", "Lincoln", "Linn", "Logan", "Lyon", "McPherson", "Marion", "Marshall", "Meade",
      "Miami", "Mitchell", "Montgomery", "Morris", "Morton", "Nemaha", "Neosho", "Ness", "Norton", "Osage",
      "Osborne", "Ottawa", "Pawnee", "Phillips", "Pottawatomie", "Pratt", "Rawlins", "Reno", "Republic", "Rice",
      "Riley", "Rooks", "Rush", "Russell", "Saline", "Scott", "Sedgwick", "Seward", "Shawnee", "Sheridan",
      "Sherman", "Smith", "Stafford", "Stanton", "Stevens", "Sumner", "Thomas", "Trego", "Wabaunsee", "Wallace",
      "Washington", "Wichita", "Wilson", "Woodson", "Wyandotte"
    ]
  },
  {
    code: "KY",
    name: "Kentucky",
    region: "South",
    capital: "Frankfort",
    sampleCity: "Louisville",
    sampleZip: "40202",
    fipsPrefix: "21",
    totalCountiesCount: 120,
    counties: [
      "Adair", "Allen", "Anderson", "Ballard", "Barren", "Bath", "Bell", "Boone", "Bourbon", "Boyd",
      "Boyle", "Bracken", "Breathitt", "Breckinridge", "Bullitt", "Butler", "Caldwell", "Calloway", "Campbell", "Carlisle",
      "Carroll", "Carter", "Casey", "Christian", "Clark", "Clay", "Clinton", "Crittenden", "Cumberland", "Daviess",
      "Edmonson", "Elliott", "Estill", "Fayette", "Fleming", "Floyd", "Franklin", "Fulton", "Gallatin", "Garrard",
      "Grant", "Graves", "Grayson", "Green", "Greenup", "Hancock", "Hardin", "Harlan", "Harrison", "Hart",
      "Henderson", "Henry", "Hickman", "Hopkins", "Jackson", "Jefferson", "Jessamine", "Johnson", "Kenton", "Knott",
      "Knox", "Larue", "Laurel", "Lawrence", "Lee", "Leslie", "Letcher", "Lewis", "Lincoln", "Livingston",
      "Logan", "Lyon", "McCracken", "McCreary", "McLean", "Madison", "Magoffin", "Marion", "Marshall", "Martin",
      "Mason", "Meade", "Menifee", "Mercer", "Metcalfe", "Monroe", "Montgomery", "Morgan", "Muhlenberg", "Nelson",
      "Nicholas", "Ohio", "Oldham", "Owen", "Owsley", "Pendleton", "Perry", "Pike", "Powell", "Pulaski",
      "Robertson", "Rockcastle", "Rowan", "Russell", "Scott", "Shelby", "Simpson", "Spencer", "Taylor", "Todd",
      "Trigg", "Trimble", "Union", "Warren", "Washington", "Wayne", "Webster", "Whitley", "Wolfe", "Woodford"
    ]
  },
  {
    code: "LA",
    name: "Louisiana",
    region: "South",
    capital: "Baton Rouge",
    sampleCity: "New Orleans",
    sampleZip: "70112",
    fipsPrefix: "22",
    totalCountiesCount: 64,
    counties: [
      "Acadia", "Allen", "Ascension", "Assumption", "Avoyelles", "Beauregard", "Bienville", "Bossier", "Caddo", "Calcasieu",
      "Caldwell", "Cameron", "Catahoula", "Claiborne", "Concordia", "DeSoto", "East Baton Rouge", "East Carroll", "East Feliciana", "Evangeline",
      "Franklin", "Grant", "Iberia", "Iberville", "Jackson", "Jefferson", "Jefferson Davis", "Lafayette", "Lafourche", "LaSalle",
      "Lincoln", "Livingston", "Madison", "Morehouse", "Natchitoches", "Orleans", "Ouachita", "Plaquemines", "Pointe Coupee", "Rapides",
      "Red River", "Richland", "Sabine", "St. Bernard", "St. Charles", "St. Helena", "St. James", "St. John the Baptist", "St. Landry", "St. Martin",
      "St. Mary", "St. Tammany", "Tangipahoa", "Tensas", "Terrebonne", "Union", "Vermilion", "Vernon", "Washington", "Webster",
      "West Baton Rouge", "West Carroll", "West Feliciana", "Winn"
    ]
  },
  {
    code: "ME",
    name: "Maine",
    region: "Northeast",
    capital: "Augusta",
    sampleCity: "Portland",
    sampleZip: "04101",
    fipsPrefix: "23",
    totalCountiesCount: 16,
    counties: [
      "Androscoggin", "Aroostook", "Cumberland", "Franklin", "Hancock", "Kennebec", "Knox", "Lincoln",
      "Oxford", "Penobscot", "Piscataquis", "Sagadahoc", "Somerset", "Waldo", "Washington", "York"
    ]
  },
  {
    code: "MD",
    name: "Maryland",
    region: "South",
    capital: "Annapolis",
    sampleCity: "Baltimore",
    sampleZip: "21201",
    fipsPrefix: "24",
    totalCountiesCount: 24,
    counties: [
      "Allegany", "Anne Arundel", "Baltimore City", "Baltimore County", "Calvert", "Caroline", "Carroll", "Cecil", "Charles", "Dorchester",
      "Frederick", "Garrett", "Harford", "Howard", "Kent", "Montgomery", "Prince George's", "Queen Anne's", "St. Mary's", "Somerset",
      "Talbot", "Washington", "Wicomico", "Worcester"
    ]
  },
  {
    code: "MA",
    name: "Massachusetts",
    region: "Northeast",
    capital: "Boston",
    sampleCity: "Boston",
    sampleZip: "02108",
    fipsPrefix: "25",
    totalCountiesCount: 14,
    counties: [
      "Barnstable", "Berkshire", "Bristol", "Dukes", "Essex", "Franklin", "Hampden", "Hampshire",
      "Middlesex", "Nantucket", "Norfolk", "Plymouth", "Suffolk", "Worcester"
    ]
  },
  {
    code: "MI",
    name: "Michigan",
    region: "Midwest",
    capital: "Lansing",
    sampleCity: "Detroit",
    sampleZip: "48226",
    fipsPrefix: "26",
    totalCountiesCount: 83,
    counties: [
      "Alcona", "Alger", "Allegan", "Alpena", "Antrim", "Arenac", "Baraga", "Barry", "Bay", "Benzie",
      "Berrien", "Branch", "Calhoun", "Cass", "Charlevoix", "Cheboygan", "Chippewa", "Clare", "Clinton", "Crawford",
      "Delta", "Dickinson", "Eaton", "Emmet", "Genesee", "Gladwin", "Gogebic", "Grand Traverse", "Gratiot", "Hillsdale",
      "Houghton", "Huron", "Ingham", "Ionia", "Iosco", "Iron", "Isabella", "Jackson", "Kalamazoo", "Kalkaska",
      "Kent", "Keweenaw", "Lake", "Lapeer", "Leelanau", "Lenawee", "Livingston", "Luce", "Mackinac", "Macomb",
      "Manistee", "Marquette", "Mason", "Mecosta", "Menominee", "Midland", "Missaukee", "Monroe", "Montcalm", "Montmorency",
      "Muskegon", "Newaygo", "Oakland", "Oceana", "Ogemaw", "Ontonagon", "Osceola", "Oscoda", "Otsego", "Ottawa",
      "Presque Isle", "Roscommon", "Saginaw", "St. Clair", "St. Joseph", "Sanilac", "Schoolcraft", "Shiawassee", "Tuscola", "Van Buren",
      "Washtenaw", "Wayne", "Wexford"
    ]
  },
  {
    code: "MN",
    name: "Minnesota",
    region: "Midwest",
    capital: "Saint Paul",
    sampleCity: "Minneapolis",
    sampleZip: "55401",
    fipsPrefix: "27",
    totalCountiesCount: 87,
    counties: [
      "Aitkin", "Anoka", "Becker", "Beltrami", "Benton", "Big Stone", "Blue Earth", "Brown", "Carlton", "Carver",
      "Cass", "Chippewa", "Chisago", "Clay", "Clearwater", "Cook", "Cottonwood", "Crow Wing", "Dakota", "Dodge",
      "Douglas", "Faribault", "Fillmore", "Freeborn", "Goodhue", "Grant", "Hennepin", "Houston", "Hubbard", "Isanti",
      "Itasca", "Jackson", "Kanabec", "Kandiyohi", "Kittson", "Koochiching", "Lac qui Parle", "Lake", "Lake of the Woods", "Le Sueur",
      "Lincoln", "Lyon", "McLeod", "Mahnomen", "Marshall", "Martin", "Meeker", "Mille Lacs", "Morrison", "Mower",
      "Murray", "Nicollet", "Nobles", "Norman", "Olmsted", "Otter Tail", "Pennington", "Pine", "Pipestone", "Polk",
      "Pope", "Ramsey", "Red Lake", "Redwood", "Renville", "Rice", "Rock", "Roseau", "St. Louis", "Scott",
      "Sherburne", "Sibley", "Stearns", "Steele", "Stevens", "Swift", "Todd", "Traverse", "Wabasha", "Wadena",
      "Waseca", "Washington", "Watonwan", "Wilkin", "Winona", "Wright", "Yellow Medicine"
    ]
  },
  {
    code: "MS",
    name: "Mississippi",
    region: "South",
    capital: "Jackson",
    sampleCity: "Jackson",
    sampleZip: "39201",
    fipsPrefix: "28",
    totalCountiesCount: 82,
    counties: [
      "Adams", "Alcorn", "Amite", "Attala", "Benton", "Bolivar", "Calhoun", "Carroll", "Chickasaw", "Choctaw",
      "Claiborne", "Clarke", "Clay", "Coahoma", "Copiah", "Covington", "DeSoto", "Forrest", "Franklin", "George",
      "Greene", "Grenada", "Hancock", "Harrison", "Hinds", "Holmes", "Humphreys", "Issaquena", "Itawamba", "Jackson",
      "Jasper", "Jefferson", "Jefferson Davis", "Jones", "Kemper", "Lafayette", "Lamar", "Lauderdale", "Lawrence", "Leake",
      "Lee", "Leflore", "Lincoln", "Lowndes", "Madison", "Marion", "Marshall", "Monroe", "Montgomery", "Neshoba",
      "Newton", "Noxubee", "Oktibbeha", "Panola", "Pearl River", "Perry", "Pike", "Pontotoc", "Prentiss", "Quitman",
      "Rankin", "Scott", "Sharkey", "Simpson", "Smith", "Stone", "Sunflower", "Tallahatchie", "Tate", "Tippah",
      "Tishomingo", "Tunica", "Union", "Walthall", "Warren", "Washington", "Wayne", "Webster", "Wilkinson", "Winston",
      "Yalobusha", "Yazoo"
    ]
  },
  {
    code: "MO",
    name: "Missouri",
    region: "Midwest",
    capital: "Jefferson City",
    sampleCity: "St. Louis",
    sampleZip: "63101",
    fipsPrefix: "29",
    totalCountiesCount: 115,
    counties: [
      "Adair", "Andrew", "Atchison", "Audrain", "Barry", "Barton", "Bates", "Benton", "Bollinger", "Boone",
      "Buchanan", "Butler", "Caldwell", "Callaway", "Camden", "Cape Girardeau", "Carroll", "Carter", "Cass", "Cedar",
      "Chariton", "Christian", "Clark", "Clay", "Clinton", "Cole", "Cooper", "Crawford", "Dade", "Dallas",
      "Daviess", "DeKalb", "Dent", "Douglas", "Dunklin", "Franklin", "Gasconade", "Gentry", "Greene", "Grundy",
      "Harrison", "Henry", "Hickory", "Holt", "Howard", "Howell", "Iron", "Jackson", "Jasper", "Jefferson",
      "Johnson", "Knox", "Laclede", "Lafayette", "Lawrence", "Lewis", "Lincoln", "Linn", "Livingston", "McDonald",
      "Macon", "Madison", "Maries", "Marion", "Mercer", "Miller", "Mississippi", "Moniteau", "Monroe", "Montgomery",
      "Morgan", "New Madrid", "Newton", "Nodaway", "Oregon", "Osage", "Ozark", "Pemiscot", "Perry", "Pettis",
      "Phelps", "Pike", "Platte", "Polk", "Pulaski", "Putnam", "Ralls", "Randolph", "Ray", "Reynolds",
      "Ripley", "St. Charles", "St. Clair", "St. Francois", "St. Louis City", "St. Louis County", "Ste. Genevieve", "Saline", "Schuyler", "Scotland",
      "Scott", "Shannon", "Shelby", "Stoddard", "Stone", "Sullivan", "Taney", "Texas", "Vernon", "Warren",
      "Washington", "Wayne", "Webster", "Worth", "Wright"
    ]
  },
  {
    code: "MT",
    name: "Montana",
    region: "West",
    capital: "Helena",
    sampleCity: "Billings",
    sampleZip: "59101",
    fipsPrefix: "30",
    totalCountiesCount: 56,
    counties: [
      "Beaverhead", "Big Horn", "Blaine", "Broadwater", "Carbon", "Carter", "Cascade", "Chouteau", "Custer", "Daniels",
      "Dawson", "Deer Lodge", "Fallon", "Fergus", "Flathead", "Gallatin", "Garfield", "Glacier", "Golden Valley", "Granite",
      "Hill", "Jefferson", "Judith Basin", "Lake", "Lewis and Clark", "Liberty", "Lincoln", "McCone", "Madison", "Meagher",
      "Mineral", "Missoula", "Musselshell", "Park", "Petroleum", "Phillips", "Pondera", "Powder River", "Powell", "Prairie",
      "Ravalli", "Richland", "Roosevelt", "Rosebud", "Sanders", "Sheridan", "Silver Bow", "Stillwater", "Sweet Grass", "Teton",
      "Toole", "Treasure", "Valley", "Wheatland", "Wibaux", "Yellowstone"
    ]
  },
  {
    code: "NE",
    name: "Nebraska",
    region: "Midwest",
    capital: "Lincoln",
    sampleCity: "Omaha",
    sampleZip: "68102",
    fipsPrefix: "31",
    totalCountiesCount: 93,
    counties: [
      "Adams", "Antelope", "Arthur", "Banner", "Blaine", "Boone", "Box Butte", "Boyd", "Brown", "Buffalo",
      "Burt", "Butler", "Cass", "Cedar", "Chase", "Cherry", "Cheyenne", "Clay", "Colfax", "Cuming",
      "Custer", "Dakota", "Dawes", "Dawson", "Deuel", "Dixon", "Dodge", "Douglas", "Dundy", "Fillmore",
      "Franklin", "Frontier", "Furnas", "Gage", "Garden", "Garfield", "Gosper", "Grant", "Greeley", "Hall",
      "Hamilton", "Harlan", "Hayes", "Hitchcock", "Holt", "Hooker", "Howard", "Jefferson", "Johnson", "Kearney",
      "Keith", "Keya Paha", "Kimball", "Knox", "Lancaster", "Lincoln", "Logan", "Loup", "McPherson", "Madison",
      "Merrick", "Morrill", "Nance", "Nemaha", "Nuckolls", "Otoe", "Pawnee", "Perkins", "Phelps", "Pierce",
      "Platte", "Polk", "Red Willow", "Richardson", "Rock", "Saline", "Sarpy", "Saunders", "Scotts Bluff", "Seward",
      "Sheridan", "Sherman", "Sioux", "Stanton", "Thayer", "Thomas", "Thurston", "Valley", "Washington", "Wayne",
      "Webster", "Wheeler", "York"
    ]
  },
  {
    code: "NV",
    name: "Nevada",
    region: "West",
    capital: "Carson City",
    sampleCity: "Las Vegas",
    sampleZip: "89101",
    fipsPrefix: "32",
    totalCountiesCount: 17,
    counties: [
      "Carson City", "Churchill", "Clark", "Douglas", "Elko", "Esmeralda", "Eureka", "Humboldt", "Lander", "Lincoln",
      "Lyon", "Mineral", "Nye", "Pershing", "Storey", "Washoe", "White Pine"
    ]
  },
  {
    code: "NH",
    name: "New Hampshire",
    region: "Northeast",
    capital: "Concord",
    sampleCity: "Manchester",
    sampleZip: "03101",
    fipsPrefix: "33",
    totalCountiesCount: 10,
    counties: [
      "Belknap", "Carroll", "Cheshire", "Coos", "Grafton", "Hillsborough", "Merrimack", "Rockingham", "Strafford", "Sullivan"
    ]
  },
  {
    code: "NJ",
    name: "New Jersey",
    region: "Northeast",
    capital: "Trenton",
    sampleCity: "Newark",
    sampleZip: "07102",
    fipsPrefix: "34",
    totalCountiesCount: 21,
    counties: [
      "Atlantic", "Bergen", "Burlington", "Camden", "Cape May", "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon",
      "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union",
      "Warren"
    ]
  },
  {
    code: "NM",
    name: "New Mexico",
    region: "West",
    capital: "Santa Fe",
    sampleCity: "Albuquerque",
    sampleZip: "87102",
    fipsPrefix: "35",
    totalCountiesCount: 33,
    counties: [
      "Bernalillo", "Catron", "Chaves", "Cibola", "Colfax", "Curry", "De Baca", "Doña Ana", "Eddy", "Grant",
      "Guadalupe", "Harding", "Hidalgo", "Lea", "Lincoln", "Los Alamos", "Luna", "McKinley", "Mora", "Otero",
      "Quay", "Rio Arriba", "Roosevelt", "Sandoval", "San Juan", "San Miguel", "Santa Fe", "Sierra", "Socorro", "Taos",
      "Torrance", "Union", "Valencia"
    ]
  },
  {
    code: "NY",
    name: "New York",
    region: "Northeast",
    capital: "Albany",
    sampleCity: "New York",
    sampleZip: "10001",
    fipsPrefix: "36",
    totalCountiesCount: 62,
    counties: [
      "Albany", "Allegany", "Bronx", "Broome", "Cattaraugus", "Cayuga", "Chautauqua", "Chemung", "Chenango", "Clinton",
      "Columbia", "Cortland", "Delaware", "Dutchess", "Erie", "Essex", "Franklin", "Fulton", "Genesee", "Greene",
      "Hamilton", "Herkimer", "Jefferson", "Kings", "Lewis", "Livingston", "Madison", "Monroe", "Montgomery", "Nassau",
      "New York", "Niagara", "Oneida", "Onondaga", "Ontario", "Orange", "Orleans", "Oswego", "Otsego", "Putnam",
      "Queens", "Rensselaer", "Richmond", "Rockland", "St. Lawrence", "Saratoga", "Schenectady", "Schoharie", "Schuyler", "Seneca",
      "Steuben", "Suffolk", "Sullivan", "Tioga", "Tompkins", "Ulster", "Warren", "Washington", "Wayne", "Westchester",
      "Wyoming", "Yates"
    ]
  },
  {
    code: "NC",
    name: "North Carolina",
    region: "South",
    capital: "Raleigh",
    sampleCity: "Charlotte",
    sampleZip: "28202",
    fipsPrefix: "37",
    totalCountiesCount: 100,
    counties: [
      "Alamance", "Alexander", "Alleghany", "Anson", "Ashe", "Avery", "Beaufort", "Bertie", "Bladen", "Brunswick",
      "Buncombe", "Burke", "Cabarrus", "Caldwell", "Camden", "Carteret", "Caswell", "Catawba", "Chatham", "Cherokee",
      "Chowan", "Clay", "Cleveland", "Columbus", "Craven", "Cumberland", "Currituck", "Dare", "Davidson", "Davie",
      "Duplin", "Durham", "Edgecombe", "Forsyth", "Franklin", "Gaston", "Gates", "Graham", "Granville", "Greene",
      "Guilford", "Halifax", "Harnett", "Haywood", "Henderson", "Hertford", "Hoke", "Hyde", "Iredell", "Jackson",
      "Johnston", "Jones", "Lee", "Lenoir", "Lincoln", "McDowell", "Macon", "Madison", "Martin", "Mecklenburg",
      "Mitchell", "Montgomery", "Moore", "Nash", "New Hanover", "Northampton", "Onslow", "Orange", "Pamlico", "Pasquotank",
      "Pender", "Perquimans", "Person", "Pitt", "Polk", "Randolph", "Richmond", "Robeson", "Rockingham", "Rowan",
      "Rutherford", "Sampson", "Scotland", "Stanly", "Stokes", "Surry", "Swain", "Transylvania", "Tyrrell", "Union",
      "Vance", "Wake", "Warren", "Washington", "Watauga", "Wayne", "Wilkes", "Wilson", "Yadkin", "Yancey"
    ]
  },
  {
    code: "ND",
    name: "North Dakota",
    region: "Midwest",
    capital: "Bismarck",
    sampleCity: "Fargo",
    sampleZip: "58102",
    fipsPrefix: "38",
    totalCountiesCount: 53,
    counties: [
      "Adams", "Barnes", "Benson", "Billings", "Bottineau", "Bowman", "Burke", "Burleigh", "Cass", "Cavalier",
      "Dickey", "Divide", "Dunn", "Eddy", "Emmons", "Foster", "Golden Valley", "Grand Forks", "Grant", "Griggs",
      "Hettinger", "Kidder", "LaMoure", "Logan", "McHenry", "McIntosh", "McKenzie", "McLean", "Mercer", "Morton",
      "Mountrail", "Nelson", "Oliver", "Pembina", "Pierce", "Ramsey", "Ransom", "Renville", "Richland", "Rolette",
      "Sargent", "Sheridan", "Sioux", "Slope", "Stark", "Steele", "Stutsman", "Towner", "Traill", "Walsh",
      "Ward", "Wells", "Williams"
    ]
  },
  {
    code: "OH",
    name: "Ohio",
    region: "Midwest",
    capital: "Columbus",
    sampleCity: "Columbus",
    sampleZip: "43215",
    fipsPrefix: "39",
    totalCountiesCount: 88,
    counties: [
      "Adams", "Allen", "Ashland", "Ashtabula", "Athens", "Auglaize", "Belmont", "Brown", "Butler", "Carroll",
      "Champaign", "Clark", "Clermont", "Clinton", "Columbiana", "Coshocton", "Crawford", "Cuyahoga", "Darke", "Defiance",
      "Delaware", "Erie", "Fairfield", "Fayette", "Franklin", "Fulton", "Gallia", "Geauga", "Greene", "Guernsey",
      "Hamilton", "Hancock", "Hardin", "Harrison", "Henry", "Highland", "Hocking", "Holmes", "Huron", "Jackson",
      "Jefferson", "Knox", "Lake", "Lawrence", "Licking", "Logan", "Lorain", "Lucas", "Madison", "Mahoning",
      "Marion", "Medina", "Meigs", "Mercer", "Miami", "Monroe", "Montgomery", "Morgan", "Morrow", "Muskingum",
      "Noble", "Ottawa", "Paulding", "Perry", "Pickaway", "Pike", "Portage", "Preble", "Putnam", "Richland",
      "Ross", "Sandusky", "Scioto", "Seneca", "Shelby", "Stark", "Summit", "Trumbull", "Tuscarawas", "Union",
      "Van Wert", "Vinton", "Warren", "Washington", "Wayne", "Williams", "Wood", "Wyandot"
    ]
  },
  {
    code: "OK",
    name: "Oklahoma",
    region: "South",
    capital: "Oklahoma City",
    sampleCity: "Oklahoma City",
    sampleZip: "73102",
    fipsPrefix: "40",
    totalCountiesCount: 77,
    counties: [
      "Adair", "Alfalfa", "Atoka", "Beaver", "Beckham", "Blaine", "Bryan", "Caddo", "Canadian", "Carter",
      "Cherokee", "Choctaw", "Cimarron", "Cleveland", "Coal", "Comanche", "Cotton", "Craig", "Creek", "Custer",
      "Delaware", "Dewey", "Ellis", "Garfield", "Garvin", "Grady", "Grant", "Greer", "Harmon", "Harper",
      "Haskell", "Hughes", "Jackson", "Jefferson", "Johnston", "Kay", "Kingfisher", "Kiowa", "Latimer", "Le Flore",
      "Lincoln", "Logan", "Love", "McClain", "McCurtain", "McIntosh", "Major", "Marshall", "Mayes", "Murray",
      "Muskogee", "Noble", "Nowata", "Okfuskee", "Oklahoma", "Okmulgee", "Osage", "Ottawa", "Pawnee", "Payne",
      "Pittsburg", "Pontotoc", "Pottawatomie", "Pushmataha", "Roger Mills", "Rogers", "Seminole", "Sequoyah", "Stephens", "Texas",
      "Tillman", "Tulsa", "Wagoner", "Washington", "Washita", "Woods", "Woodward"
    ]
  },
  {
    code: "OR",
    name: "Oregon",
    region: "West",
    capital: "Salem",
    sampleCity: "Portland",
    sampleZip: "97201",
    fipsPrefix: "41",
    totalCountiesCount: 36,
    counties: [
      "Baker", "Benton", "Clackamas", "Clatsop", "Columbia", "Coos", "Crook", "Curry", "Deschutes", "Douglas",
      "Gilliam", "Grant", "Harney", "Hood River", "Jackson", "Jefferson", "Josephine", "Klamath", "Lake", "Lane",
      "Lincoln", "Linn", "Malheur", "Marion", "Morrow", "Multnomah", "Polk", "Sherman", "Tillamook", "Umatilla",
      "Union", "Wallowa", "Wasco", "Washington", "Wheeler", "Yamhill"
    ]
  },
  {
    code: "PA",
    name: "Pennsylvania",
    region: "Northeast",
    capital: "Harrisburg",
    sampleCity: "Philadelphia",
    sampleZip: "19102",
    fipsPrefix: "42",
    totalCountiesCount: 67,
    counties: [
      "Adams", "Allegheny", "Armstrong", "Beaver", "Bedford", "Berks", "Blair", "Bradford", "Bucks", "Butler",
      "Cambria", "Cameron", "Carbon", "Centre", "Chester", "Clarion", "Clearfield", "Clinton", "Columbia", "Crawford",
      "Cumberland", "Dauphin", "Delaware", "Elk", "Erie", "Fayette", "Forest", "Franklin", "Fulton", "Greene",
      "Huntingdon", "Indiana", "Jefferson", "Juniata", "Lackawanna", "Lancaster", "Lawrence", "Lebanon", "Lehigh", "Luzerne",
      "Lycoming", "McKean", "Mercer", "Mifflin", "Monroe", "Montgomery", "Montour", "Northampton", "Northumberland", "Perry",
      "Philadelphia", "Pike", "Potter", "Schuylkill", "Snyder", "Somerset", "Sullivan", "Susquehanna", "Tioga", "Union",
      "Venango", "Warren", "Washington", "Wayne", "Westmoreland", "Wyoming", "York"
    ]
  },
  {
    code: "RI",
    name: "Rhode Island",
    region: "Northeast",
    capital: "Providence",
    sampleCity: "Providence",
    sampleZip: "02903",
    fipsPrefix: "44",
    totalCountiesCount: 5,
    counties: [
      "Bristol", "Kent", "Newport", "Providence", "Washington"
    ]
  },
  {
    code: "SC",
    name: "South Carolina",
    region: "South",
    capital: "Columbia",
    sampleCity: "Charleston",
    sampleZip: "29401",
    fipsPrefix: "45",
    totalCountiesCount: 46,
    counties: [
      "Abbeville", "Aiken", "Allendale", "Anderson", "Bamberg", "Barnwell", "Beaufort", "Berkeley", "Calhoun", "Charleston",
      "Cherokee", "Chester", "Chesterfield", "Clarendon", "Colleton", "Darlington", "Dillon", "Dorchester", "Edgefield", "Fairfield",
      "Florence", "Georgetown", "Greenville", "Greenwood", "Hampton", "Horry", "Jasper", "Kershaw", "Lancaster", "Laurens",
      "Lee", "Lexington", "McCormick", "Marion", "Marlboro", "Newberry", "Oconee", "Orangeburg", "Pickens", "Richland",
      "Saluda", "Spartanburg", "Sumter", "Union", "Williamsburg", "York"
    ]
  },
  {
    code: "SD",
    name: "South Dakota",
    region: "Midwest",
    capital: "Pierre",
    sampleCity: "Sioux Falls",
    sampleZip: "57104",
    fipsPrefix: "46",
    totalCountiesCount: 66,
    counties: [
      "Aurora", "Beadle", "Bennett", "Bon Homme", "Brookings", "Brown", "Brule", "Buffalo", "Butte", "Campbell",
      "Charles Mix", "Clark", "Clay", "Codington", "Corson", "Custer", "Davison", "Day", "Deuel", "Dewey",
      "Douglas", "Edmunds", "Fall River", "Faulk", "Grant", "Gregory", "Haakon", "Hamlin", "Hand", "Hanson",
      "Harding", "Hughes", "Hutchinson", "Hyde", "Jackson", "Jerauld", "Jones", "Kingsbury", "Lake", "Lawrence",
      "Lincoln", "Lyman", "McCook", "McPherson", "Marshall", "Meade", "Mellette", "Miner", "Minnehaha", "Moody",
      "Oglala Lakota", "Pennington", "Perkins", "Potter", "Roberts", "Sanborn", "Spink", "Stanley", "Sully", "Todd",
      "Tripp", "Turner", "Union", "Walworth", "Yankton", "Ziebach"
    ]
  },
  {
    code: "TN",
    name: "Tennessee",
    region: "South",
    capital: "Nashville",
    sampleCity: "Nashville",
    sampleZip: "37201",
    fipsPrefix: "47",
    totalCountiesCount: 95,
    counties: [
      "Anderson", "Bedford", "Benton", "Bledsoe", "Blount", "Bradley", "Campbell", "Cannon", "Carroll", "Carter",
      "Cheatham", "Chester", "Claiborne", "Clay", "Cocke", "Coffee", "Crockett", "Cumberland", "Davidson", "Decatur",
      "DeKalb", "Dickson", "Dyer", "Fayette", "Fentress", "Franklin", "Gibson", "Giles", "Grainger", "Greene",
      "Grundy", "Hamblen", "Hamilton", "Hancock", "Hardeman", "Hardin", "Hawkins", "Haywood", "Henderson", "Henry",
      "Hickman", "Houston", "Humphreys", "Jackson", "Jefferson", "Johnson", "Knox", "Lake", "Lauderdale", "Lawrence",
      "Lewis", "Lincoln", "Loudon", "McMinn", "McNairy", "Macon", "Madison", "Marion", "Marshall", "Maury",
      "Meigs", "Monroe", "Montgomery", "Moore", "Morgan", "Obion", "Overton", "Perry", "Pickett", "Polk",
      "Putnam", "Rhea", "Roane", "Robertson", "Rutherford", "Scott", "Sequatchie", "Sevier", "Shelby", "Smith",
      "Stewart", "Sullivan", "Sumner", "Tipton", "Trousdale", "Unicoi", "Union", "Van Buren", "Warren", "Washington",
      "Wayne", "Weakley", "White", "Williamson", "Wilson"
    ]
  },
  {
    code: "TX",
    name: "Texas",
    region: "South",
    capital: "Austin",
    sampleCity: "Austin",
    sampleZip: "78701",
    fipsPrefix: "48",
    totalCountiesCount: 254,
    counties: [
      "Anderson", "Andrews", "Angelina", "Aransas", "Archer", "Armstrong", "Atascosa", "Austin", "Bailey", "Bandera",
      "Bastrop", "Baylor", "Bee", "Bell", "Bexar", "Blanco", "Borden", "Bosque", "Bowie", "Brazoria",
      "Brazos", "Brewster", "Briscoe", "Brooks", "Brown", "Burleson", "Burnet", "Caldwell", "Calhoun", "Callahan",
      "Cameron", "Camp", "Carson", "Cass", "Castro", "Chambers", "Cherokee", "Childress", "Clay", "Cochran",
      "Coke", "Coleman", "Collin", "Collingsworth", "Colorado", "Comal", "Comanche", "Concho", "Cooke", "Coryell",
      "Cottle", "Crane", "Crockett", "Crosby", "Culberson", "Dallam", "Dallas", "Dawson", "Deaf Smith", "Delta",
      "Denton", "DeWitt", "Dickens", "Dimmit", "Donley", "Duval", "Eastland", "Ector", "Edwards", "Ellis",
      "El Paso", "Erath", "Falls", "Fannin", "Fayette", "Fisher", "Floyd", "Foard", "Fort Bend", "Franklin",
      "Freestone", "Frio", "Gaines", "Galveston", "Garza", "Gillespie", "Glasscock", "Goliad", "Gonzales", "Gray",
      "Grayson", "Gregg", "Grimes", "Guadalupe", "Hale", "Hall", "Hamilton", "Hansford", "Hardeman", "Hardin",
      "Harris", "Harrison", "Hartley", "Haskell", "Hays", "Hemphill", "Henderson", "Hidalgo", "Hill", "Hockley",
      "Hood", "Hopkins", "Houston", "Howard", "Hudspeth", "Hunt", "Hutchinson", "Irion", "Jack", "Jackson",
      "Jasper", "Jeff Davis", "Jefferson", "Jim Hogg", "Jim Wells", "Johnson", "Jones", "Karnes", "Kaufman", "Kendall",
      "Kenedy", "Kent", "Kerr", "Kimble", "King", "Kinney", "Kleberg", "Knox", "Lamar", "Lamb",
      "Lampasas", "La Salle", "Lavaca", "Lee", "Leon", "Liberty", "Limestone", "Lipscomb", "Live Oak", "Llano",
      "Loving", "Lubbock", "Lynn", "McCulloch", "McLennan", "McMullen", "Madison", "Marion", "Martin", "Mason",
      "Matagorda", "Maverick", "Medina", "Menard", "Midland", "Milam", "Mills", "Mitchell", "Montague", "Montgomery",
      "Moore", "Morris", "Motley", "Nacogdoches", "Navarro", "Newton", "Nolan", "Nueces", "Ochiltree", "Oldham",
      "Orange", "Palo Pinto", "Panola", "Parker", "Parmer", "Pecos", "Polk", "Potter", "Presidio", "Rains",
      "Randall", "Reagan", "Real", "Red River", "Reeves", "Refugio", "Roberts", "Robertson", "Rockwall", "Runnels",
      "Rusk", "Sabine", "San Augustine", "San Jacinto", "San Patricio", "San Saba", "Schleicher", "Scurry", "Shackelford", "Shelby",
      "Sherman", "Smith", "Somervell", "Starr", "Stephens", "Sterling", "Stonewall", "Sutton", "Swisher", "Tarrant",
      "Taylor", "Terrell", "Terry", "Throckmorton", "Titus", "Tom Green", "Travis", "Trinity", "Tyler", "Upshur",
      "Upton", "Uvalde", "Val Verde", "Van Zandt", "Victoria", "Walker", "Waller", "Ward", "Washington", "Webb",
      "Wharton", "Wheeler", "Wichita", "Wilbarger", "Willacy", "Williamson", "Wilson", "Winkler", "Wise", "Wood",
      "Yoakum", "Young", "Zapata", "Zavala"
    ]
  },
  {
    code: "UT",
    name: "Utah",
    region: "West",
    capital: "Salt Lake City",
    sampleCity: "Salt Lake City",
    sampleZip: "84101",
    fipsPrefix: "49",
    totalCountiesCount: 29,
    counties: [
      "Beaver", "Box Elder", "Cache", "Carbon", "Daggett", "Davis", "Duchesne", "Emery", "Garfield", "Grand",
      "Iron", "Juab", "Kane", "Millard", "Morgan", "Piute", "Rich", "Salt Lake", "San Juan", "Sanpete",
      "Sevier", "Summit", "Tooele", "Uintah", "Utah", "Wasatch", "Washington", "Wayne", "Weber"
    ]
  },
  {
    code: "VT",
    name: "Vermont",
    region: "Northeast",
    capital: "Montpelier",
    sampleCity: "Burlington",
    sampleZip: "05401",
    fipsPrefix: "50",
    totalCountiesCount: 14,
    counties: [
      "Addison", "Bennington", "Caledonia", "Chittenden", "Essex", "Franklin", "Grand Isle", "Lamoille",
      "Orange", "Orleans", "Rutland", "Washington", "Windham", "Windsor"
    ]
  },
  {
    code: "VA",
    name: "Virginia",
    region: "South",
    capital: "Richmond",
    sampleCity: "Richmond",
    sampleZip: "23219",
    fipsPrefix: "51",
    totalCountiesCount: 133,
    counties: [
      "Accomack", "Albemarle", "Alexandria City", "Alleghany", "Amelia", "Amherst", "Appomattox", "Arlington", "Augusta", "Bath",
      "Bedford", "Bland", "Botetourt", "Bristol City", "Brunswick", "Buchanan", "Buckingham", "Buena Vista City", "Campbell", "Caroline",
      "Carroll", "Charles City", "Charlotte", "Charlottesville City", "Chesapeake City", "Chesterfield", "Clarke", "Colonial Heights City", "Covington City", "Craig",
      "Culpeper", "Cumberland", "Danville City", "Dickenson", "Dinwiddie", "Emporia City", "Essex", "Fairfax City", "Fairfax County", "Falls Church City",
      "Fauquier", "Floyd", "Fluvanna", "Franklin City", "Franklin County", "Frederick", "Fredericksburg City", "Galax City", "Giles", "Gloucester",
      "Goochland", "Grayson", "Greene", "Greensville", "Halifax", "Hampton City", "Hanover", "Harrisonburg City", "Henrico", "Henry",
      "Highland", "Hopewell City", "Isle of Wight", "James City", "King and Queen", "King George", "King William", "Lancaster", "Lee", "Lexington City",
      "Loudoun", "Louisa", "Lunenburg", "Lynchburg City", "Madison", "Manassas City", "Manassas Park City", "Martinsville City", "Mathews", "Mecklenburg",
      "Middlesex", "Montgomery", "Nelson", "New Kent", "Newport News City", "Norfolk City", "Northampton", "Northumberland", "Norton City", "Nottoway",
      "Orange", "Page", "Patrick", "Petersburg City", "Pittsylvania", "Poquoson City", "Portsmouth City", "Powhatan", "Prince Edward", "Prince George",
      "Prince William", "Pulaski", "Radford City", "Rappahannock", "Richmond City", "Richmond County", "Roanoke City", "Roanoke County", "Rockbridge", "Rockingham",
      "Russell", "Salem City", "Scott", "Shenandoah", "Smyth", "Southampton", "Spotsylvania", "Stafford", "Staunton City", "Suffolk City",
      "Surry", "Sussex", "Tazewell", "Virginia Beach City", "Warren", "Washington", "Waynesboro City", "Westmoreland", "Williamsburg City", "Winchester City",
      "Wise", "Wythe", "York"
    ]
  },
  {
    code: "WA",
    name: "Washington",
    region: "West",
    capital: "Olympia",
    sampleCity: "Seattle",
    sampleZip: "98101",
    fipsPrefix: "53",
    totalCountiesCount: 39,
    counties: [
      "Adams", "Asotin", "Benton", "Chelan", "Clallam", "Clark", "Columbia", "Cowlitz", "Douglas", "Ferry",
      "Franklin", "Garfield", "Grant", "Grays Harbor", "Island", "Jefferson", "King", "Kitsap", "Kittitas", "Klickitat",
      "Lewis", "Lincoln", "Mason", "Okanogan", "Pacific", "Pend Oreille", "Pierce", "San Juan", "Skagit", "Skamania",
      "Snohomish", "Spokane", "Stevens", "Thurston", "Wahkiakum", "Walla Walla", "Whatcom", "Whitman", "Yakima"
    ]
  },
  {
    code: "WV",
    name: "West Virginia",
    region: "South",
    capital: "Charleston",
    sampleCity: "Charleston",
    sampleZip: "25301",
    fipsPrefix: "54",
    totalCountiesCount: 55,
    counties: [
      "Barbour", "Berkeley", "Boone", "Braxton", "Brooke", "Cabell", "Calhoun", "Clay", "Doddridge", "Fayette",
      "Gilmer", "Grant", "Greenbrier", "Hampshire", "Hancock", "Hardy", "Harrison", "Jackson", "Jefferson", "Kanawha",
      "Lewis", "Lincoln", "Logan", "McDowell", "Marion", "Marshall", "Mason", "Mercer", "Mineral", "Mingo",
      "Monongalia", "Monroe", "Morgan", "Nicholas", "Ohio", "Pendleton", "Pleasants", "Pocahontas", "Preston", "Putnam",
      "Raleigh", "Randolph", "Ritchie", "Roane", "Summers", "Taylor", "Tucker", "Tyler", "Upshur", "Wayne",
      "Webster", "Wetzel", "Wirt", "Wood", "Wyoming"
    ]
  },
  {
    code: "WI",
    name: "Wisconsin",
    region: "Midwest",
    capital: "Madison",
    sampleCity: "Milwaukee",
    sampleZip: "53202",
    fipsPrefix: "55",
    totalCountiesCount: 72,
    counties: [
      "Adams", "Ashland", "Barron", "Bayfield", "Brown", "Buffalo", "Burnett", "Calumet", "Chippewa", "Clark",
      "Columbia", "Crawford", "Dane", "Dodge", "Door", "Douglas", "Dunn", "Eau Claire", "Florence", "Fond du Lac",
      "Forest", "Grant", "Green", "Green Lake", "Iowa", "Iron", "Jackson", "Jefferson", "Juneau", "Kenosha",
      "Kewaunee", "La Crosse", "Lafayette", "Langlade", "Lincoln", "Manitowoc", "Marathon", "Marinette", "Marquette", "Menominee",
      "Milwaukee", "Monroe", "Oconto", "Oneida", "Outagamie", "Ozaukee", "Pepin", "Pierce", "Polk", "Portage",
      "Price", "Racine", "Richland", "Rock", "Rusk", "St. Croix", "Sauk", "Sawyer", "Shawano", "Sheboygan",
      "Taylor", "Trempealeau", "Vernon", "Vilas", "Walworth", "Washburn", "Washington", "Waukesha", "Waupaca", "Waushara",
      "Winnebago", "Wood"
    ]
  },
  {
    code: "WY",
    name: "Wyoming",
    region: "West",
    capital: "Cheyenne",
    sampleCity: "Cheyenne",
    sampleZip: "82001",
    fipsPrefix: "56",
    totalCountiesCount: 23,
    counties: [
      "Albany", "Big Horn", "Campbell", "Carbon", "Converse", "Crook", "Fremont", "Goshen", "Hot Springs", "Johnson",
      "Laramie", "Lincoln", "Natrona", "Niobrara", "Park", "Platte", "Sheridan", "Sublette", "Sweetwater", "Teton",
      "Uinta", "Washakie", "Weston"
    ]
  }
];

export function slugifyCounty(text: string): string {
  return text.toLowerCase()
    .replace(/\s+(county|parish|borough|city)\b/gi, "")
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "") || "county";
}

export const slugify = slugifyCounty;

export function getNetrCountyUrl(stateCode: string, countyName: string): string {
  return `https://publicrecords.netronline.com/state/${stateCode.toUpperCase()}/county/${slugifyCounty(countyName)}`;
}

export function getNetrStateUrl(stateCode: string): string {
  return `https://publicrecords.netronline.com/state/${stateCode.toUpperCase()}`;
}

export function getNetrGisUrl(stateCode: string, countyName: string): string {
  return `https://map.netronline.com/${stateCode.toLowerCase()}-${slugifyCounty(countyName)}`;
}


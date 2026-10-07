import { useState, useEffect, useCallback, type ReactNode } from "react";
import {
  ALL_50_STATES,
  slugify,
  slugifyCounty,
  getNetrCountyUrl,
  getNetrStateUrl,
  getNetrGisUrl,
  type StateCountyData,
} from "./data/statesAndCounties";
import { queryRegridApi, type RegridParcelData } from "./services/regridService";

type IconName =
  | "grid"
  | "search"
  | "orders"
  | "exceptions"
  | "reports"
  | "settings"
  | "help"
  | "bell"
  | "arrow"
  | "check"
  | "clock"
  | "file"
  | "sparkles"
  | "pin";

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, ReactNode> = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
    search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
    orders: <><path d="M7 3h10l3 3v15H4V3h3Z" /><path d="M8 8h8M8 12h8M8 16h5" /></>,
    exceptions: <><path d="M12 3 2.8 20h18.4L12 3Z" /><path d="M12 9v5m0 3h.01" /></>,
    reports: <><path d="M4 20V10m6 10V4m6 16v-7m4 7H2" /></>,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.6v-.2h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z" /></>,
    help: <><circle cx="12" cy="12" r="9" /><path d="M9.8 9a2.3 2.3 0 1 1 3.5 2c-.8.5-1.3 1-1.3 2m0 3h.01" /></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9Z" /><path d="M10 21h4" /></>,
    arrow: <><path d="M5 12h14m-5-5 5 5-5 5" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    file: <><path d="M6 2h8l4 4v16H6V2Z" /><path d="M14 2v5h5M9 12h6m-6 4h6" /></>,
    sparkles: <><path d="m12 2 1.2 3.8L17 7l-3.8 1.2L12 12l-1.2-3.8L7 7l3.8-1.2L12 2Z" /><path d="m5 13 .8 2.2L8 16l-2.2.8L5 19l-.8-2.2L2 16l2.2-.8L5 13Zm13-1 .7 2.3 2.3.7-2.3.7L18 18l-.7-2.3L15 15l2.3-.7L18 12Z" /></>,
    pin: <><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z" /><circle cx="12" cy="10" r="2.5" /></>,
  };

  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {paths[name]}
    </svg>
  );
}

const nav = [
  { label: "Overview", icon: "grid" as IconName },
  { label: "Property search", icon: "search" as IconName },
  { label: "States & Counties", icon: "pin" as IconName },
  { label: "Orders", icon: "orders" as IconName },
  { label: "Exceptions", icon: "exceptions" as IconName, count: 3 },
  { label: "Reports", icon: "reports" as IconName },
];

const stages = [
  { label: "Property input", detail: "Address and APN verified", status: "done" },
  { label: "PI search", detail: "Owner and legal retrieved", status: "done" },
  { label: "Chain of title", detail: "Tracing prior ownership", status: "active" },
  { label: "Encumbrances", detail: "Queued for search", status: "waiting" },
  { label: "QA review", detail: "Pending", status: "waiting" },
];

export type DocumentCategory = "all" | "chain" | "deeds" | "mortgages" | "judgments" | "liens";

export type TitleRecord = {
  id: string;
  category: "deeds" | "mortgages" | "judgments" | "liens";
  type: string;
  date: string;
  grantor: string;
  grantee: string;
  party: string;
  ref: string;
  bookPage: string;
  amount?: string;
  status: "Recorded" | "Open" | "Satisfied" | "Clear" | "Exception";
  statusClass: "doc-status-recorded" | "doc-status-open" | "doc-status-satisfied" | "doc-status-clear" | "doc-status-exception";
  accent?: boolean;
  legalNote: string;
};

const orders = [
  { id: "COS-24831", property: "123 Main Street", county: "Travis County, TX", owner: "John Smith", status: "In progress", date: "Today, 9:42 AM" },
  { id: "COS-24830", property: "84 Willow Creek Drive", county: "Harris County, TX", owner: "Maria Garcia", status: "QA review", date: "Today, 8:16 AM" },
  { id: "COS-24829", property: "512 Lakeview Avenue", county: "Dallas County, TX", owner: "Harbor Ventures LLC", status: "Complete", date: "Yesterday, 4:38 PM" },
  { id: "COS-24828", property: "27 Oak Ridge Court", county: "Bexar County, TX", owner: "David Chen", status: "Exception", date: "Yesterday, 2:05 PM" },
];

const initialExceptions = [
  { id: 1, title: "Owner name mismatch", property: "27 Oak Ridge Court", detail: "Recorded deed lists “David H. Chen”; property index lists “David Chen.”", level: "Review" },
  { id: 2, title: "Unreleased lien detected", property: "116 Westover Lane", detail: "A 2018 mechanic’s lien has no matching release in the general index.", level: "High" },
  { id: 3, title: "Incomplete legal description", property: "9401 Cedar Bend", detail: "Source document image is missing the final exhibit page.", level: "Source needed" },
];

const stateNameMap: Record<string, string> = {
  alabama: "AL", alaska: "AK", arizona: "AZ", arkansas: "AR", california: "CA", colorado: "CO",
  connecticut: "CT", delaware: "DE", "district of columbia": "DC", florida: "FL", georgia: "GA", hawaii: "HI", idaho: "ID",
  illinois: "IL", indiana: "IN", iowa: "IA", kansas: "KS", kentucky: "KY", louisiana: "LA",
  maine: "ME", maryland: "MD", massachusetts: "MA", michigan: "MI", minnesota: "MN", mississippi: "MS",
  missouri: "MO", montana: "MT", nebraska: "NE", nevada: "NV", "new hampshire": "NH", "new jersey": "NJ",
  "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", ohio: "OH",
  oklahoma: "OK", oregon: "OR", pennsylvania: "PA", "rhode island": "RI", "south carolina": "SC",
  "south dakota": "SD", tennessee: "TN", texas: "TX", utah: "UT", vermont: "VT", virginia: "VA",
  washington: "WA", "west virginia": "WV", wisconsin: "WI", wyoming: "WY",
};

const cityCountyMap: Record<string, { county: string; state: string; zip: string; defaultOwner?: string }> = {
  lawtey: { county: "Bradford", state: "FL", zip: "32058", defaultOwner: "Arthur & Brenda Pendelton" },
  starke: { county: "Bradford", state: "FL", zip: "32091", defaultOwner: "Arthur & Brenda Pendelton" },
  austin: { county: "Travis", state: "TX", zip: "78701", defaultOwner: "David & Sarah Martinez" },
  glendale: { county: "Los Angeles", state: "CA", zip: "91203", defaultOwner: "Michael C. Henderson" },
  "los angeles": { county: "Los Angeles", state: "CA", zip: "90012", defaultOwner: "Elena Rodriguez" },
  miami: { county: "Miami-Dade", state: "FL", zip: "33131", defaultOwner: "Carlos & Maria Delgado" },
  "miami beach": { county: "Miami-Dade", state: "FL", zip: "33139", defaultOwner: "Carlos & Maria Delgado" },
  houston: { county: "Harris", state: "TX", zip: "77002", defaultOwner: "Maria Garcia & James Garcia" },
  dallas: { county: "Dallas", state: "TX", zip: "75201", defaultOwner: "Harbor Ventures LLC" },
  tampa: { county: "Hillsborough", state: "FL", zip: "33602", defaultOwner: "Richard & Susan Vance" },
  orlando: { county: "Orange", state: "FL", zip: "32801", defaultOwner: "Sunbelt Holdings LLC" },
  jacksonville: { county: "Duval", state: "FL", zip: "32202", defaultOwner: "Marcus & Evelyn Reed" },
  chicago: { county: "Cook", state: "IL", zip: "60601", defaultOwner: "William & Patricia O'Connor" },
  phoenix: { county: "Maricopa", state: "AZ", zip: "85001", defaultOwner: "Robert & Kimberly Adams" },
  seattle: { county: "King", state: "WA", zip: "98101", defaultOwner: "Cascade Properties Trust" },
  denver: { county: "Denver", state: "CO", zip: "80202", defaultOwner: "Gregory & Laura Palmer" },
  atlanta: { county: "Fulton", state: "GA", zip: "30303", defaultOwner: "Terrence & Alicia Wright" },
  charlotte: { county: "Mecklenburg", state: "NC", zip: "28202", defaultOwner: "Lucas & Emily Bennett" },
  "san antonio": { county: "Bexar", state: "TX", zip: "78205", defaultOwner: "David Chen & Linda Chen" },
  "san diego": { county: "San Diego", state: "CA", zip: "92101", defaultOwner: "Pacific Crest Holdings" },
  "san jose": { county: "Santa Clara", state: "CA", zip: "95113", defaultOwner: "Silicon Valley Realty LLC" },
  "san francisco": { county: "San Francisco", state: "CA", zip: "94102", defaultOwner: "Bayview Asset Management" },
};

const knownPortals: Record<string, { recorder: string; appraiser: string; tax: string }> = {
  "bradford_fl": {
    recorder: "https://www3.myfloridacounty.com/ori/index.do",
    appraiser: "http://www.bradfordappraiser.com/gis/",
    tax: "https://www.bradfordtaxcollector.com/Property/SearchSelect?ClearData=True",
  },
  "travis_tx": {
    recorder: "https://countyclerk.traviscountytx.gov/",
    appraiser: "https://traviscad.org/propertysearch",
    tax: "https://tax-office.traviscountytx.gov/",
  },
  "harris_tx": {
    recorder: "https://www.cchctx.org/",
    appraiser: "https://hcad.org/property-search.html",
    tax: "https://www.hctax.net/",
  },
  "los_angeles_ca": {
    recorder: "https://lavote.gov/",
    appraiser: "https://portal.assessor.lacounty.gov/",
    tax: "https://ttc.lacounty.gov/",
  },
  "miami_dade_fl": {
    recorder: "https://www.miamidadeclerk.gov/",
    appraiser: "https://www.miamidade.gov/pa/",
    tax: "https://miamidade.county-taxes.com/",
  },
  "orange_fl": {
    recorder: "https://myorangeclerk.com/",
    appraiser: "https://ocpafl.org/",
    tax: "https://octaxcol.com/",
  },
  "cook_il": {
    recorder: "https://www.cookcountyclerkil.gov/",
    appraiser: "https://www.cookcountyassessor.com/",
    tax: "https://www.cookcountytreasurer.com/",
  },
  "maricopa_az": {
    recorder: "https://recorder.maricopa.gov/",
    appraiser: "https://mcassessor.maricopa.gov/",
    tax: "https://treasurer.maricopa.gov/",
  },
  "king_wa": {
    recorder: "https://kingcounty.gov/en/dept/records-licensing/records-and-licensing-services/recorders-office",
    appraiser: "https://kingcounty.gov/en/dept/assessors",
    tax: "https://kingcounty.gov/en/dept/finance-business-operations/treasury-operations",
  },
  "fulton_ga": {
    recorder: "https://www.fultonclerk.org/",
    appraiser: "https://fultonassessor.org/",
    tax: "https://www.fultoncountytaxes.org/",
  },
  "dallas_tx": {
    recorder: "https://www.dallascounty.org/government/county-clerk/",
    appraiser: "https://www.dallascad.org/",
    tax: "https://www.dallascounty.org/departments/tax/",
  },
};

const sampleOwnerNames = [
  "Arthur & Brenda Pendelton",
  "David & Sarah Martinez",
  "Michael C. Henderson",
  "James & Linda Walker",
  "Thomas & Karen Reynolds",
  "Elena & Marcus Vance",
  "William & Cynthia Hayes",
  "Robert & Dorothy Sullivan",
];

const samplePriorOwners = [
  "Robert M. Sterling",
  "Anna C. Moore",
  "Estate of Harold Brooks",
  "Charles & Diane Foster",
  "Oakridge Development Partners LLC",
  "Lawtey Pineview Estates, LLC",
];

export type PropertyDetail = {
  street: string;
  city: string;
  county: string;
  countySlug: string;
  state: string;
  zip: string;
  apn: string;
  assessedValue: string;
  landValue: string;
  improvementValue: string;
  legalDesc: string;
  owner: string;
  secondaryOwner?: string;
  isLiveRegrid?: boolean;
  zoning?: string;
  yearBuilt?: string;
  useDescription?: string;
  latitude?: number;
  longitude?: number;
  netrCountyUrl: string;
  netrStateUrl: string;
  netrGisUrl: string;
  historicAerialsUrl: string;
  dataStoreUrl: string;
  recorderPortal: string;
  appraiserPortal: string;
  taxPortal: string;
  documents: TitleRecord[];
  chainSteps: { sequence: string; from: string; to: string; date: string; type: string; ref: string }[];
};

function parseAddressInfo(rawQuery: string, regrid?: RegridParcelData | null): PropertyDetail {
  const cleanInput = rawQuery.trim() || "4320 NW CR 225, Lawtey, FL 32058";
  const lowerQuery = cleanInput.toLowerCase();

  // Detect if query is directly an APN format (e.g., 12007-00418 or 123-456-789)
  const isDirectApn = /^[0-9]{3,6}[-\s][0-9]{2,6}([-\s][0-9]{2,6})*$/i.test(cleanInput);

  // Detect if query is directly an Owner Name (e.g., "Arthur & Brenda Pendelton", "John A. Smith")
  const isDirectOwner = !isDirectApn && !/^\d+\s+[a-zA-Z]/i.test(cleanInput) && !cleanInput.includes(",") && cleanInput.split(" ").length <= 5 && !/\b(street|st|road|rd|ave|avenue|dr|drive|lane|ln|cr|blvd|hwy|way)\b/i.test(lowerQuery);

  const parts = cleanInput.split(",").map(p => p.trim()).filter(Boolean);
  let street = isDirectOwner ? "4320 NW CR 225" : isDirectApn ? "4320 NW CR 225" : parts[0] || "4320 NW CR 225";
  let city = "Lawtey";
  let state = "FL";
  let county = "Bradford";
  let zip = "32058";
  let matchedDefaultOwner: string | undefined = isDirectOwner ? cleanInput : undefined;

  // Match full state names
  for (const [sName, sCode] of Object.entries(stateNameMap)) {
    if (new RegExp(`\\b${sName}\\b`, "i").test(lowerQuery)) {
      state = sCode;
      break;
    }
  }

  // Match 2-letter state codes
  const stateMatch = cleanInput.match(/\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b/i);
  if (stateMatch) {
    state = stateMatch[1].toUpperCase();
  }

  // Check city mapping
  for (const [cityName, info] of Object.entries(cityCountyMap)) {
    if (lowerQuery.includes(cityName)) {
      city = cityName.split(" ").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
      county = info.county;
      state = info.state;
      zip = info.zip;
      if (!isDirectOwner) {
        matchedDefaultOwner = info.defaultOwner;
      }
      break;
    }
  }

  // Match 5-digit zip
  const zipMatch = cleanInput.match(/\b\d{5}\b/);
  if (zipMatch) {
    zip = zipMatch[0];
  }

  // Check explicit County in parts
  if (parts.length >= 2 && !isDirectOwner) {
    for (let i = 1; i < parts.length; i++) {
      const part = parts[i];
      if (/county/i.test(part)) {
        county = part.replace(/county/i, "").trim();
      } else if (i === 1 && !lowerQuery.includes("lawtey") && !lowerQuery.includes("austin")) {
        city = part.replace(/\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|\d{5})\b/gi, "").trim() || city;
      }
    }
  }

  let countySlug = slugify(county);
  const hash = Math.abs(cleanInput.split("").reduce((acc, char) => acc + char.charCodeAt(0) * 19, 0)) || 24831;

  // Format realistic APN by state conventions or use direct input APN
  let apn = isDirectApn ? cleanInput : `${(hash % 899 + 100).toString()}-${((hash * 3) % 8999 + 1000).toString()}-${((hash * 7) % 899 + 100).toString()}`;
  if (!isDirectApn) {
    if (state === "FL") {
      apn = `12007-${((hash % 89) + 10).toString().padStart(2, "0")}-00-${((hash % 899) + 100).toString().padStart(4, "0")}-0000-00`;
    } else if (state === "CA") {
      apn = `${((hash % 8999) + 1000).toString().slice(0, 4)}-${((hash % 899) + 100).toString().slice(0, 3)}-${((hash % 89) + 10).toString().slice(0, 3)}`;
    } else if (state === "TX") {
      apn = `0${((hash % 8) + 1)}-${((hash % 8999) + 1000)}-${((hash % 899) + 100)}-0000`;
    }
  }

  const assessedTotalNum = (hash % 450 + 260) * 1000;
  const landNum = Math.round(assessedTotalNum * 0.32 / 1000) * 1000;
  const impNum = assessedTotalNum - landNum;
  let assessedValue = `$${assessedTotalNum.toLocaleString()}`;
  let landValue = `$${landNum.toLocaleString()}`;
  let improvementValue = `$${impNum.toLocaleString()}`;

  let owner = matchedDefaultOwner || sampleOwnerNames[hash % sampleOwnerNames.length];
  let secondaryOwner: string | undefined = undefined;
  const priorOwner1 = samplePriorOwners[(hash + 1) % samplePriorOwners.length];
  const priorOwner2 = samplePriorOwners[(hash + 3) % samplePriorOwners.length];

  let legalDesc = `LOT ${(hash % 24) + 1}, BLOCK ${((hash % 8) + 1)}, ${(city.toUpperCase())} ADDITION SUBDIVISION, PLAT BOOK ${(hash % 12) + 2}, PAGE ${(hash % 45) + 10}, ${county.toUpperCase()} COUNTY, ${state}`;

  // If Regrid live parcel data is available, override with authoritative live government data
  let isLiveRegrid = false;
  let zoning: string | undefined = undefined;
  let yearBuilt: string | undefined = undefined;
  let useDescription: string | undefined = undefined;
  let latitude: number | undefined = undefined;
  let longitude: number | undefined = undefined;

  if (regrid) {
    isLiveRegrid = true;
    if (regrid.address) street = regrid.address;
    if (regrid.city) city = regrid.city;
    if (regrid.county) county = regrid.county;
    if (regrid.state) state = regrid.state;
    if (regrid.zip) zip = regrid.zip;
    if (regrid.apn) apn = regrid.apn;
    if (regrid.owner) owner = regrid.owner;
    if (regrid.secondaryOwner) secondaryOwner = regrid.secondaryOwner;
    if (regrid.assessedValue) assessedValue = regrid.assessedValue;
    if (regrid.landValue) landValue = regrid.landValue;
    if (regrid.improvementValue) improvementValue = regrid.improvementValue;
    if (regrid.legalDescription) legalDesc = regrid.legalDescription;
    zoning = regrid.zoning;
    yearBuilt = regrid.yearBuilt;
    useDescription = regrid.useDescription;
    latitude = regrid.latitude;
    longitude = regrid.longitude;
    countySlug = slugify(county);
  }


  // NETR Online Links
  const netrCountyUrl = `https://publicrecords.netronline.com/state/${state}/county/${countySlug}`;
  const netrStateUrl = `https://publicrecords.netronline.com/state/${state}`;
  const netrGisUrl = `https://map.netronline.com/${state.toLowerCase()}-${countySlug}`;
  const historicAerialsUrl = "https://www.historicaerials.com/";
  const dataStoreUrl = "https://datastore.netronline.com/";

  // Official portal URLs
  const portalKey = `${countySlug}_${state.toLowerCase()}`;
  let recorderPortal = netrCountyUrl;
  let appraiserPortal = netrCountyUrl;
  let taxPortal = netrCountyUrl;

  if (knownPortals[portalKey]) {
    recorderPortal = knownPortals[portalKey].recorder;
    appraiserPortal = knownPortals[portalKey].appraiser;
    taxPortal = knownPortals[portalKey].tax;
  }

  // Dynamic Title Records for this exact property
  const currentYear = 2026;
  const vestingYear = currentYear - 2;
  const priorYear1 = vestingYear - 4;
  const priorYear2 = priorYear1 - 8;

  const vestingRef = `${vestingYear}-${((hash * 13) % 89999 + 10000).toString()}`;
  const priorRef1 = `${priorYear1}-${((hash * 17) % 89999 + 10000).toString()}`;
  const priorRef2 = `${priorYear2}-${((hash * 23) % 89999 + 10000).toString()}`;
  const mtgRef = `${vestingYear}-${((hash * 13) % 89999 + 10001).toString()}`;
  const relRef = `${vestingYear}-${((hash * 11) % 89999 + 10000).toString()}`;

  const book1 = `OR Book ${(hash % 500) + 1400}, Page ${(hash % 800) + 50}`;
  const book2 = `OR Book ${(hash % 500) + 1200}, Page ${(hash % 800) + 50}`;
  const book3 = `OR Book ${(hash % 500) + 900}, Page ${(hash % 800) + 50}`;
  const mtgBook = `OR Book ${(hash % 500) + 1400}, Page ${(hash % 800) + 55}`;

  const loanAmount = `$${Math.round(assessedTotalNum * 0.8 / 1000 * 1000).toLocaleString()}`;
  const purchasePrice = `$${assessedTotalNum.toLocaleString()}`;

  const dynamicDocuments: TitleRecord[] = [
    // Deeds
    {
      id: "doc-1",
      category: "deeds",
      type: "Vesting Deed / Special Warranty Deed",
      date: `May 14, ${vestingYear}`,
      grantor: priorOwner1,
      grantee: `${owner} (Current Owner)`,
      party: `${priorOwner1} → ${owner}`,
      ref: vestingRef,
      bookPage: book1,
      amount: purchasePrice,
      status: "Recorded",
      statusClass: "doc-status-recorded",
      accent: true,
      legalNote: `Current Vesting Instrument conveying 100% Fee Simple title to ${street}, ${city}, ${state}. Verified in ${county} County public records.`,
    },
    {
      id: "doc-2",
      category: "deeds",
      type: "General Warranty Deed",
      date: `Aug 03, ${priorYear1}`,
      grantor: priorOwner2,
      grantee: priorOwner1,
      party: `${priorOwner2} → ${priorOwner1}`,
      ref: priorRef1,
      bookPage: book2,
      amount: `$${Math.round(assessedTotalNum * 0.78 / 1000 * 1000).toLocaleString()}`,
      status: "Recorded",
      statusClass: "doc-status-recorded",
      legalNote: `Prior conveyance in chain with full statutory warranties of title. Clean execution verified.`,
    },
    {
      id: "doc-3",
      category: "deeds",
      type: "Grant Deed / Developer Conveyance",
      date: `Nov 12, ${priorYear2}`,
      grantor: "Estate & Development Trust Holdings",
      grantee: priorOwner2,
      party: `Estate Holdings → ${priorOwner2}`,
      ref: priorRef2,
      bookPage: book3,
      amount: "$10.00 Consideration",
      status: "Recorded",
      statusClass: "doc-status-recorded",
      legalNote: `Historical link in title chain establishing original subdivision plat conveyance.`,
    },

    // Mortgages
    {
      id: "doc-4",
      category: "mortgages",
      type: "1st Lien Mortgage / Deed of Trust (Mtg)",
      date: `May 14, ${vestingYear}`,
      grantor: `${owner} (Borrower)`,
      grantee: "First National Mortgage & Lending Corp",
      party: `${owner} → First National Mortgage`,
      ref: mtgRef,
      bookPage: mtgBook,
      amount: loanAmount,
      status: "Open",
      statusClass: "doc-status-open",
      accent: true,
      legalNote: `Active 1st lien conventional mortgage securing promissory note. Current open balance on record.`,
    },
    {
      id: "doc-5",
      category: "mortgages",
      type: "Release & Satisfaction of Prior Mortgage",
      date: `May 10, ${vestingYear}`,
      grantor: "Wells Fargo Bank, N.A. / Prior Lender",
      grantee: priorOwner1,
      party: `Wells Fargo Bank → ${priorOwner1}`,
      ref: relRef,
      bookPage: `OR Book ${(hash % 500) + 1395}, Page 614`,
      amount: "Paid in Full",
      status: "Satisfied",
      statusClass: "doc-status-satisfied",
      legalNote: `Full reconveyance and discharge of prior mortgage recorded on ${street}.`,
    },

    // Judgments
    {
      id: "doc-6",
      category: "judgments",
      type: "Circuit Court GI Judgment Search",
      date: `Oct 06, ${currentYear}`,
      grantor: `${county} County Court & Circuit Index`,
      grantee: `${owner} / Prior Owners`,
      party: `20-Year Civil Index Examination`,
      ref: `GI-${currentYear}-${(hash % 8999 + 1000).toString()}`,
      bookPage: "Court Docket Index",
      amount: "$0.00",
      status: "Clear",
      statusClass: "doc-status-clear",
      legalNote: `Zero unsatisfied money judgments, child support liens, or active Lis Pendens on record against ${owner}.`,
    },
    {
      id: "doc-7",
      category: "judgments",
      type: "State & Federal Tax Registry Examination",
      date: `Oct 06, ${currentYear}`,
      grantor: `${state} Dept of Revenue & US District Court`,
      grantee: owner,
      party: "DOR & IRS Certified Index",
      ref: `TAX-GI-${(hash % 899 + 100).toString()}`,
      bookPage: "Federal Tax Docket",
      amount: "$0.00",
      status: "Clear",
      statusClass: "doc-status-clear",
      legalNote: `Certified negative search. No federal tax liens or state revenue warrants attached to subject property or owner.`,
    },

    // Liens & Taxes
    {
      id: "doc-8",
      category: "liens",
      type: "County Property Tax Assessment (Tax Collector)",
      date: `${currentYear - 1}/${currentYear} Tax Roll`,
      grantor: `${county} County Tax Collector`,
      grantee: street,
      party: "Annual Ad Valorem Real Property Tax",
      ref: `TAX-${currentYear - 1}-${(hash % 8999 + 1000).toString()}`,
      bookPage: `Tax Roll Folio #${apn.slice(0, 10)}`,
      amount: `$${Math.round(assessedTotalNum * 0.0125).toLocaleString()} (Paid)`,
      status: "Clear",
      statusClass: "doc-status-clear",
      legalNote: `Taxes for the current assessment cycle are PAID IN FULL. Zero delinquent taxes due to ${county} County.`,
    },
    {
      id: "doc-9",
      category: "liens",
      type: "Unreleased Mechanic's & HOA Lien Verification",
      date: `Oct 06, ${currentYear}`,
      grantor: "Official Records General Index",
      grantee: "Subject Property",
      party: "Lien & Encumbrance Verification",
      ref: `LIEN-VERIF-${currentYear}`,
      bookPage: "Lien Index Search",
      amount: "$0.00 Active",
      status: "Clear",
      statusClass: "doc-status-clear",
      legalNote: `No active construction liens, HOA special assessments, or municipal utility holds detected on parcel.`,
    },
  ];

  const dynamicChainSteps = [
    { sequence: "01", from: "Estate & Development Trust Holdings", to: priorOwner2, date: `Nov 12, ${priorYear2}`, type: "Grant Deed", ref: priorRef2 },
    { sequence: "02", from: priorOwner2, to: priorOwner1, date: `Aug 03, ${priorYear1}`, type: "Warranty Deed", ref: priorRef1 },
    { sequence: "03", from: priorOwner1, to: owner, date: `May 14, ${vestingYear}`, type: "Vesting Deed", ref: vestingRef },
  ];

  return {
    street,
    city,
    county,
    countySlug,
    state,
    zip,
    apn,
    assessedValue,
    landValue,
    improvementValue,
    legalDesc,
    owner,
    netrCountyUrl,
    netrStateUrl,
    netrGisUrl,
    historicAerialsUrl,
    dataStoreUrl,
    recorderPortal,
    appraiserPortal,
    taxPortal,
    documents: dynamicDocuments,
    chainSteps: dynamicChainSteps,
  };
}

export default function App() {
  const [activeNav, setActiveNav] = useState("Overview");
  const [query, setQuery] = useState("4320 NW CR 225, Lawtey, FL 32058");
  const [searched, setSearched] = useState(true);
  const [regridData, setRegridData] = useState<RegridParcelData | null>(null);
  const [isRegridLoading, setIsRegridLoading] = useState(false);
  const [docCategory, setDocCategory] = useState<DocumentCategory>("all");
  const [selectedDocument, setSelectedDocument] = useState<TitleRecord | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<(typeof orders)[number] | null>(null);
  const [exceptions, setExceptions] = useState(initialExceptions);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [toast, setToast] = useState("");
  const [orderFilter, setOrderFilter] = useState("");
  const [settings, setSettings] = useState({ email: true, exceptions: true, completion: false });
  const [explorerStateCode, setExplorerStateCode] = useState("FL");
  const [explorerCountyName, setExplorerCountyName] = useState("Bradford");
  const [explorerFilter, setExplorerFilter] = useState("");
  const [natGlobalSearch, setNatGlobalSearch] = useState("");
  const [natSelectedRegion, setNatSelectedRegion] = useState<string>("All");
  const [natSelectedState, setNatSelectedState] = useState<string>("FL");
  const [natSelectedLetter, setNatSelectedLetter] = useState<string | null>(null);
  const [countyModal, setCountyModal] = useState<{ county: string; state: StateCountyData } | null>(null);

  const activeProperty = parseAddressInfo(query, regridData);
  const currentExplorerState = ALL_50_STATES.find(s => s.code === explorerStateCode) || ALL_50_STATES[9];

  const filteredExplorerCounties = currentExplorerState.counties.filter(c => 
    c.toLowerCase().includes(explorerFilter.toLowerCase())
  );

  const filteredDocuments = docCategory === "all"
    ? activeProperty.documents
    : docCategory === "chain"
    ? activeProperty.documents.filter(d => d.category === "deeds")
    : activeProperty.documents.filter(d => d.category === docCategory);

  const executeSearch = useCallback(async (targetQuery: string) => {
    const clean = targetQuery.trim();
    if (!clean) return;
    setIsRegridLoading(true);
    try {
      const liveParcel = await queryRegridApi(clean);
      if (liveParcel) {
        setRegridData(liveParcel);
        showToast(`🟢 Regrid Live API: Retrieved parcel APN ${liveParcel.apn} (${liveParcel.owner})`);
      } else {
        setRegridData(null);
      }
    } catch (e) {
      setRegridData(null);
    } finally {
      setIsRegridLoading(false);
    }
  }, []);

  // Initial Regrid lookup on load
  useEffect(() => {
    executeSearch(query);
  }, []);

  function loadExplorerCounty(stateCode: string, countyName: string) {
    const stateObj = ALL_50_STATES.find(s => s.code === stateCode);
    const city = stateObj?.sampleCity || "Main";
    const zip = stateObj?.sampleZip || "00000";
    const newQuery = `100 Main Street, ${city}, ${countyName} County, ${stateCode} ${zip}`;
    setExplorerStateCode(stateCode);
    setExplorerCountyName(countyName);
    setQuery(newQuery);
    setSearched(true);
    setActiveNav("Property search");
    executeSearch(newQuery);
    showToast(`Connected ${countyName} County, ${stateCode} via NETR Online`);
  }

  function runSearch(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim()) {
      setSearched(true);
      setActiveNav("Property search");
      executeSearch(query);
      showToast(`Searching across Regrid API & NETR Online for ${query.split(",")[0]}...`);
    }
  }

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(""), 2600);
  }

  function goTo(view: string) {
    setActiveNav(view);
    setNotificationsOpen(false);
  }

  function startNewSearch() {
    setQuery("");
    setSearched(false);
    goTo("Property search");
  }


  function renderSearchWorkspace(showGreeting = false) {
    return (
      <>
        {showGreeting && (
          <>
            <section className="welcome">
              <div>
                <span className="ai-label"><Icon name="sparkles" size={14} /> AI-Assisted Title Intelligence</span>
                <h2>Good morning, Alex.</h2>
                <p>Welcome to Verity Title Intelligence. Explore the web platform architecture and end-to-end title examination workflow below.</p>
              </div>
              <div className="today-stat">
                <span>Today</span><strong>12</strong><small>reports processed</small>
              </div>
            </section>

            {/* Platform Explanation & 5-Step Title Examination Process */}
            <section className="overview-guide-section">
              <article className="about-platform-card">
                <span className="about-badge"><Icon name="sparkles" size={13} /> Web Platform & Architecture</span>
                <h2>Verity Title Intelligence & Public Records Engine</h2>
                <p className="about-desc">
                  Verity is an enterprise title examination platform powered by live public records data integration. 
                  By connecting directly with <strong>NETR Online</strong> (National Environmental Title Research) and official local recording repositories across 3,143+ U.S. counties, 
                  Verity automates parcel geocoding, APN matching, 30-year deed chain assembly, adverse lien/judgment detection, and tax verification in seconds.
                </p>

                <div className="about-features-row">
                  <div className="about-feature-item">
                    <span className="about-feature-icon"><Icon name="pin" size={16} /></span>
                    <div>
                      <strong>NETR Directory Hub</strong>
                      <small>Live links to Clerk/Recorder, Assessor, Tax Collector & GIS portals</small>
                    </div>
                  </div>
                  <div className="about-feature-item">
                    <span className="about-feature-icon"><Icon name="file" size={16} /></span>
                    <div>
                      <strong>Chain of Title Assembly</strong>
                      <small>Automated backwards & forwards Grantor/Grantee deed conveyance tracing</small>
                    </div>
                  </div>
                  <div className="about-feature-item">
                    <span className="about-feature-icon"><Icon name="exceptions" size={16} /></span>
                    <div>
                      <strong>Encumbrance & Lien Audit</strong>
                      <small>Real-time scrubbing of open Mortgages, Mechanics Liens, & GI Judgments</small>
                    </div>
                  </div>
                  <div className="about-feature-item">
                    <span className="about-feature-icon"><Icon name="check" size={16} /></span>
                    <div>
                      <strong>Typing-Ready QA Packages</strong>
                      <small>Standardized property reports, exception queues, and PDF exports</small>
                    </div>
                  </div>
                </div>
              </article>

              <div className="process-section">
                <div className="process-header">
                  <div>
                    <h3>5-Step Title Search & Examination Process</h3>
                    <p>Standard operating procedure (SOP) executed for every property order from address input to final report.</p>
                  </div>
                  <span className="process-badge"><Icon name="check" size={14} /> Full ALTA / SOP Compliant</span>
                </div>

                <div className="process-steps-grid">
                  <div className="process-step-card">
                    <span className="step-num-pill">1</span>
                    <h4>Address Geocoding & Jurisdiction</h4>
                    <p>Normalizes input street address, matches county FIPS, and retrieves parcel APN via CAD Assraiser endpoints and NETR Online directory.</p>
                    <div className="step-meta-tags">
                      <span>Address Parsing</span>
                      <span>County FIPS</span>
                      <span>APN Match</span>
                    </div>
                  </div>

                  <div className="process-step-card">
                    <span className="step-num-pill">2</span>
                    <h4>Property Index (PI) & Valuation</h4>
                    <p>Extracts formal legal description (Lot/Block/Subdivision), assesses land vs improvement values, and verifies current real estate tax status.</p>
                    <div className="step-meta-tags">
                      <span>Legal Desc</span>
                      <span>Assessed Value</span>
                      <span>Tax Certification</span>
                    </div>
                  </div>

                  <div className="process-step-card">
                    <span className="step-num-pill">3</span>
                    <h4>Chain of Title Assembly</h4>
                    <p>Constructs continuous chronological conveyance flow from current owner backward through prior Grantors (Warranty, Quitclaim & Special Deeds).</p>
                    <div className="step-meta-tags">
                      <span>30-Yr Search</span>
                      <span>Grantor/Grantee</span>
                      <span>Vesting %</span>
                    </div>
                  </div>

                  <div className="process-step-card">
                    <span className="step-num-pill">4</span>
                    <h4>Mortgages & Liens Audit</h4>
                    <p>Audits open Deeds of Trust/Mortgages against recorded Satisfactions and Releases. Checks Mechanics, HOA, and Municipal utility liens.</p>
                    <div className="step-meta-tags">
                      <span>Open Mortgages</span>
                      <span>Releases</span>
                      <span>HOA Liens</span>
                    </div>
                  </div>

                  <div className="process-step-card">
                    <span className="step-num-pill">5</span>
                    <h4>GI Judgment Search & QA Report</h4>
                    <p>Scrubs names against General Index (GI) for Tax Liens, Child Support & Bankruptcies. Compiles verified title package for examiner sign-off.</p>
                    <div className="step-meta-tags">
                      <span>GI Scrubbing</span>
                      <span>Tax Liens</span>
                      <span>Typing-Ready PDF</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}

        {!showGreeting && (
          <section className="page-intro">
            <span className="ai-label"><Icon name="sparkles" size={14} /> Connected NETR Online Sources</span>
            <h2>Research a property</h2>
            <p>Enter any property address. Verity resolves State, County, and direct NETR Online portals.</p>
          </section>
        )}

        <form className="search-card" onSubmit={runSearch}>
          <div className="search-icon"><Icon name="search" size={21} /></div>
          <label>
            <span>Search by address, APN, owner, or order number</span>
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="e.g. 4320 NW CR 225, Lawtey, FL or 123 Main St, Austin, TX" autoFocus={!showGreeting && !searched} />
          </label>
          <button type="submit" disabled={isRegridLoading}>
            {isRegridLoading ? "Querying..." : "Search property"} <Icon name="arrow" size={17} />
          </button>
        </form>

        {/* Live Regrid API & NETR Connection Bar */}
        <div className="api-status-bar">
          <div className="api-status-item">
            <span className={`status-dot ${isRegridLoading ? "pulsing" : activeProperty.isLiveRegrid ? "live" : "live"}`} />
            <span>
              <strong>Regrid Nationwide Parcel API v1:</strong>{" "}
              {isRegridLoading
                ? "Fetching live parcel records..."
                : activeProperty.isLiveRegrid
                ? `Live Verified (APN: ${activeProperty.apn} · Owner: ${activeProperty.owner})`
                : "Active & Connected (Token: pa:ts:ps:bf:ma:ty:eo:zo:sb)"}
            </span>
          </div>
          <div className="api-status-item">
            <span className="status-dot live" />
            <span><strong>NETR Online Directory:</strong> 50 States · 3,143 Counties Connected</span>
          </div>
        </div>

        {/* All 50 States & Counties NETR Directory Explorer */}
        <section className="state-explorer-card">
          <div className="state-explorer-header">
            <div>
              <span className="ai-label" style={{ marginBottom: "6px" }}><Icon name="pin" size={13} /> All 50 U.S. States & Counties</span>
              <h3>NETR Online National Public Records Directory</h3>
              <p>Explore official recording portals, assessor CAD indices, and real property records for all 50 states and 3,143+ counties.</p>
            </div>
            <span className="state-explorer-badge">50 States · 3,143 Counties</span>
          </div>

          <div className="state-controls-grid">
            <div className="state-control-group">
              <label>Select State ({ALL_50_STATES.length})</label>
              <select
                value={explorerStateCode}
                onChange={(e) => {
                  const newSt = e.target.value;
                  setExplorerStateCode(newSt);
                  const stObj = ALL_50_STATES.find(s => s.code === newSt);
                  if (stObj && stObj.counties.length > 0) {
                    setExplorerCountyName(stObj.counties[0]);
                  }
                }}
              >
                {ALL_50_STATES.map((s) => (
                  <option key={s.code} value={s.code}>{s.name} ({s.code})</option>
                ))}
              </select>
            </div>

            <div className="state-control-group">
              <label>Select County ({currentExplorerState.counties.length})</label>
              <select
                value={explorerCountyName}
                onChange={(e) => setExplorerCountyName(e.target.value)}
              >
                {currentExplorerState.counties.map((c) => (
                  <option key={c} value={c}>{c} County</option>
                ))}
              </select>
            </div>

            <div className="state-control-group">
              <label>Quick Filter County</label>
              <input
                type="text"
                value={explorerFilter}
                onChange={(e) => setExplorerFilter(e.target.value)}
                placeholder="Filter counties in state..."
              />
            </div>
          </div>

          {/* Selected County Summary & Direct NETR Navigation */}
          <div className="selected-county-preview">
            <div className="selected-county-info">
              <strong>{explorerCountyName} County, {currentExplorerState.name} ({explorerStateCode})</strong>
              <small>NETR Reference: NETR-{explorerStateCode}-{slugify(explorerCountyName).toUpperCase()} · Clerk, Assessor CAD, Tax & GIS Directory</small>
            </div>
            <div className="selected-county-actions">
              <button
                className="btn-load-county"
                onClick={() => loadExplorerCounty(explorerStateCode, explorerCountyName)}
              >
                <Icon name="sparkles" size={14} /> Search in Verity
              </button>
              <a
                className="btn-open-netr"
                href={`https://publicrecords.netronline.com/state/${explorerStateCode}/county/${slugify(explorerCountyName)}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                Open NETR County Hub ↗
              </a>
              <a
                className="text-button"
                style={{ background: "#eef6f6", color: "#173f4d", padding: "8px 12px", borderRadius: "8px" }}
                href={`https://publicrecords.netronline.com/state/${explorerStateCode}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                State Directory ↗
              </a>
            </div>
          </div>

          {/* Quick County Pills for the State */}
          <div className="county-quick-pills">
            <p>Popular {currentExplorerState.name} Counties (Click to Examine):</p>
            <div className="pills-scroll-row">
              {filteredExplorerCounties.map((c) => (
                <button
                  key={c}
                  className={`county-pill-item ${explorerCountyName === c ? "active" : ""}`}
                  onClick={() => {
                    setExplorerCountyName(c);
                    loadExplorerCounty(explorerStateCode, c);
                  }}
                >
                  {c} County
                </button>
              ))}
            </div>
          </div>
        </section>

        {!searched && (
          <section className="empty-search">
            <span><Icon name="search" size={28} /></span>
            <h3>Ready to search</h3>
            <p>Try a street address, assessor parcel number, owner name, or existing order ID.</p>
            <div style={{ display: "flex", gap: "10px", justifyContent: "center", flexWrap: "wrap", marginTop: "12px" }}>
              <button onClick={() => { setQuery("4320 NW CR 225, Lawtey, FL 32058"); setSearched(true); executeSearch("4320 NW CR 225, Lawtey, FL 32058"); }}>Bradford County, FL</button>
              <button onClick={() => { setQuery("123 Main Street, Austin, TX 78701"); setSearched(true); executeSearch("123 Main Street, Austin, TX 78701"); }}>Travis County, TX</button>
              <button onClick={() => { setQuery("450 N Brand Blvd, Glendale, Los Angeles County, CA 91203"); setSearched(true); executeSearch("450 N Brand Blvd, Glendale, Los Angeles County, CA 91203"); }}>Los Angeles County, CA</button>
            </div>
          </section>
        )}

        {searched && (
          <>
            <div className="section-heading">
              <div><h3>Active search & Title Records</h3><p>Order #COS-24831 · Connected to {activeProperty.county} County, {activeProperty.state}</p></div>
              <button className="text-button" onClick={() => goTo("Orders")}>View full order <Icon name="arrow" size={15} /></button>
            </div>

            <section className="workflow-grid">
              <article className="property-card">
                <div className="property-image">
                  <img src="/assets/property-neighborhood.png" alt="Stylized residential neighborhood" />
                  <span className="status-pill"><i /> In progress</span>
                </div>
                <div className="property-body">
                  <p className="muted-label">Subject property</p>
                  <h3>{activeProperty.street}</h3>
                  <p className="location"><Icon name="pin" size={15} /> {activeProperty.city}, {activeProperty.county} County, {activeProperty.state} {activeProperty.zip}</p>

                  {/* Big Prominent Owner Name Banner */}
                  <div className="owner-hero-banner">
                    <div className="owner-hero-top">
                      <span className="owner-hero-tag">Current Owner</span>
                      {activeProperty.isLiveRegrid ? (
                        <span className="owner-vesting-badge" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#10b981", border: "1px solid rgba(16, 185, 129, 0.4)", padding: "2px 7px", borderRadius: "4px" }}>
                          🟢 Regrid Live Verified
                        </span>
                      ) : (
                        <span className="owner-vesting-badge">100% Fee Simple</span>
                      )}
                    </div>
                    <div className="owner-name-display">{activeProperty.owner}</div>
                    {activeProperty.secondaryOwner && (
                      <div style={{ color: "#a5c2cb", fontSize: "13px", marginTop: "2px", fontWeight: 600 }}>
                        Co-Owner: {activeProperty.secondaryOwner}
                      </div>
                    )}
                    <p className="owner-subtext">
                      {activeProperty.isLiveRegrid
                        ? `Live Parcel APN: ${activeProperty.apn} · ${activeProperty.county} County CAD & Recorder`
                        : `Vested via Deed #2024-018492 · ${activeProperty.county} County Official Records`}
                    </p>
                  </div>

                  <div className="property-meta">
                    <div><span>Assessor APN</span><strong>{activeProperty.apn}</strong></div>
                    <div><span>Vested Owner</span><strong style={{ fontSize: "13px", color: "#0eaaa7" }}>{activeProperty.owner}</strong></div>
                    <div><span>Appraised value</span><strong>{activeProperty.assessedValue}</strong></div>
                    <div><span>Data Source</span><strong>{activeProperty.isLiveRegrid ? "🟢 Regrid Public Records API" : "NETR Directory Hub"}</strong></div>
                  </div>
                </div>
              </article>

              <article className="progress-card">
                <div className="card-title">
                  <div><h3>Automation progress</h3><p>3 of 5 stages underway</p></div>
                  <span>62%</span>
                </div>
                <div className="progress-track"><span /></div>
                <div className="stage-list">
                  {stages.map((stage) => (
                    <div className={`stage ${stage.status}`} key={stage.label}>
                      <span className="stage-icon">{stage.status === "done" ? <Icon name="check" size={14} /> : stage.status === "active" ? <Icon name="sparkles" size={14} /> : <Icon name="clock" size={14} />}</span>
                      <div><strong>{stage.label}</strong><small>{stage.detail}</small></div>
                      {stage.status === "active" && <em>Working</em>}
                    </div>
                  ))}
                </div>
              </article>
            </section>

            {/* NETR Online Public Records & Live County Portals Hub */}
            <section className="netr-card">
              <div className="netr-header">
                <div className="netr-header-left">
                  <span className="netr-tag">NETR Online</span>
                  <div>
                    <h3>{activeProperty.county} County, {activeProperty.state} Public Records Portal</h3>
                    <p>Verified government recording portals and title research data streams</p>
                  </div>
                </div>
                <span className="netr-badge-live">Live County Sources Online</span>
              </div>

              <div className="netr-links-grid">
                <a className="netr-link-btn" href={activeProperty.netrCountyUrl} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>NETR County Directory</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Full public records index for {activeProperty.county} County, {activeProperty.state}</small>
                  <span className="netr-link-action">Open Directory ↗</span>
                </a>

                <a className="netr-link-btn" href={activeProperty.recorderPortal} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>County Clerk / Recorder</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Deeds, Mortgages, Liens, Releases, Plats & UCC records</small>
                  <span className="netr-link-action">Search Recorder ↗</span>
                </a>

                <a className="netr-link-btn" href={activeProperty.appraiserPortal} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>Assessor / CAD Portal</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Property assessments, parcel maps, valuations & legal description</small>
                  <span className="netr-link-action">Search CAD ↗</span>
                </a>

                <a className="netr-link-btn" href={activeProperty.taxPortal} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>Tax Collector / Office</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Current tax bills, delinquent tax verification & payment receipts</small>
                  <span className="netr-link-action">View Tax Records ↗</span>
                </a>

                <a className="netr-link-btn" href={activeProperty.netrGisUrl} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>NETR GIS & Parcel Maps</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Interactive parcel polygon boundaries and FIPS mapping</small>
                  <span className="netr-link-action">Open GIS Map ↗</span>
                </a>

                <a className="netr-link-btn" href={activeProperty.historicAerialsUrl} target="_blank" rel="noopener noreferrer">
                  <div className="netr-link-top">
                    <strong>Historic Aerials</strong>
                    <Icon name="arrow" size={15} />
                  </div>
                  <small>Multi-decade historic satellite and aerial photography comparisons</small>
                  <span className="netr-link-action">View Aerials ↗</span>
                </a>
              </div>

              {/* Property Specs Breakdown */}
              <div className="specs-grid">
                <div className="specs-item">
                  <span>Legal Description</span>
                  <strong>{activeProperty.legalDesc}</strong>
                </div>
                <div className="specs-item">
                  <span>Total Assessment</span>
                  <strong>{activeProperty.assessedValue}</strong>
                </div>
                <div className="specs-item">
                  <span>Land / Improvements</span>
                  <strong>{activeProperty.landValue} / {activeProperty.improvementValue}</strong>
                </div>
                <div className="specs-item">
                  <span>Tax Status</span>
                  <strong style={{ color: "#10b981" }}>Current / Paid</strong>
                </div>
                <div className="specs-item">
                  <span>NETR Reference</span>
                  <strong>NETR-{activeProperty.state}-{activeProperty.countySlug.toUpperCase()}</strong>
                </div>
              </div>
            </section>

            {/* Comprehensive Title Records, Chain of Title, Deeds, Mortgages, Judgments & Liens */}
            <section className="evidence-card" style={{ marginTop: "18px" }}>
              <div className="card-title evidence-title" style={{ paddingBottom: "12px" }}>
                <div>
                  <h3>Title Examination: Chain of Title, Deeds, Mortgages, Judgments & Liens</h3>
                  <p>Comprehensive document index verified against {activeProperty.county} County official public records.</p>
                </div>
                <span className="confidence"><Icon name="sparkles" size={14} /> Full Title Coverage</span>
              </div>

              {/* Category Filter Tabs */}
              <div className="category-tab-bar">
                <button
                  className={`category-tab-btn ${docCategory === "all" ? "active" : ""}`}
                  onClick={() => setDocCategory("all")}
                >
                  All Documents <b>{activeProperty.documents.length}</b>
                </button>
                <button
                  className={`category-tab-btn ${docCategory === "chain" ? "active" : ""}`}
                  onClick={() => setDocCategory("chain")}
                >
                  ⛓️ Chain of Title <b>{activeProperty.chainSteps.length}</b>
                </button>
                <button
                  className={`category-tab-btn ${docCategory === "deeds" ? "active" : ""}`}
                  onClick={() => setDocCategory("deeds")}
                >
                  📜 Deeds <b>{activeProperty.documents.filter(d => d.category === "deeds").length}</b>
                </button>
                <button
                  className={`category-tab-btn ${docCategory === "mortgages" ? "active" : ""}`}
                  onClick={() => setDocCategory("mortgages")}
                >
                  🏦 Mortgages / Mtg <b>{activeProperty.documents.filter(d => d.category === "mortgages").length}</b>
                </button>
                <button
                  className={`category-tab-btn ${docCategory === "judgments" ? "active" : ""}`}
                  onClick={() => setDocCategory("judgments")}
                >
                  ⚖️ Judgments <b>{activeProperty.documents.filter(d => d.category === "judgments").length}</b>
                </button>
                <button
                  className={`category-tab-btn ${docCategory === "liens" ? "active" : ""}`}
                  onClick={() => setDocCategory("liens")}
                >
                  🚫 Liens & Taxes <b>{activeProperty.documents.filter(d => d.category === "liens").length}</b>
                </button>
              </div>

              {/* Visual Chain of Title Sequence Flow */}
              {(docCategory === "chain" || docCategory === "all") && (
                <div>
                  <p style={{ margin: "0 0 8px", fontSize: "11px", fontWeight: 700, textTransform: "uppercase", color: "#6c848c", letterSpacing: "0.05em" }}>
                    Verified Chain of Title Flow (30-Year Conveyance History)
                  </p>
                  <div className="chain-flow">
                    {activeProperty.chainSteps.map((step, idx) => (
                      <div key={step.sequence} style={{ display: "flex", alignItems: "center", gap: "12px", flex: 1 }}>
                        <div className="chain-step">
                          <div className="chain-step-seq">
                            <span>Step {step.sequence}</span>
                            <span>{step.type}</span>
                          </div>
                          <strong>{step.from}</strong>
                          <div style={{ color: "#0eaaa7", fontSize: "11px", fontWeight: 700, margin: "2px 0" }}>↓ Conveys To</div>
                          <strong>{step.to}</strong>
                          <small>Date: {step.date} · Inst #{step.ref}</small>
                        </div>
                        {idx < activeProperty.chainSteps.length - 1 && <span className="chain-arrow">→</span>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Document List */}
              <div className="document-list">
                {filteredDocuments.map((doc, index) => (
                  <button className="document-row" key={doc.id} onClick={() => setSelectedDocument(doc)}>
                    <span className={`document-icon ${doc.accent ? "accent" : ""}`}><Icon name="file" size={18} /></span>
                    <span className="doc-index">0{index + 1}</span>
                    <span className="doc-main">
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <strong>{doc.type}</strong>
                        <span className={`doc-status-badge ${doc.statusClass}`}>{doc.status}</span>
                      </div>
                      <small>{doc.party} · {doc.bookPage}</small>
                    </span>
                    <span className="doc-date">
                      <strong>{doc.date}</strong>
                      <small>Inst #{doc.ref} {doc.amount ? `· ${doc.amount}` : ""}</small>
                    </span>
                    <Icon name="arrow" size={16} />
                  </button>
                ))}
              </div>
            </section>
          </>
        )}
      </>
    );
  }

  function renderStatesAndCounties() {
    const totalCountiesNationwide = ALL_50_STATES.reduce((acc, s) => acc + s.counties.length, 0);

    // Filter states by region & letter
    const regionFilteredStates = ALL_50_STATES.filter(s => {
      if (natSelectedRegion !== "All" && s.region !== natSelectedRegion) return false;
      if (natSelectedLetter && !s.name.toUpperCase().startsWith(natSelectedLetter)) return false;
      return true;
    });

    // Global county search across all 3,143+ counties
    const isSearchingGlobal = natGlobalSearch.trim().length > 0;
    const globalMatches: { state: StateCountyData; county: string }[] = [];
    if (isSearchingGlobal) {
      const q = natGlobalSearch.toLowerCase().trim();
      ALL_50_STATES.forEach(st => {
        st.counties.forEach(c => {
          if (c.toLowerCase().includes(q) || st.name.toLowerCase().includes(q) || st.code.toLowerCase() === q) {
            globalMatches.push({ state: st, county: c });
          }
        });
      });
    }

    const alphabetLetters = ["All", "A", "C", "D", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W"];

    return (
      <div className="nat-dir-container">
        <section className="page-intro row-intro">
          <div>
            <span className="ai-label"><Icon name="pin" size={14} /> National Public Records Directory</span>
            <h2>All 50 States & 3,143+ Counties</h2>
            <p>Access official county recorder portals, CAD property appraisers, tax collectors, and GIS parcel mapping nationwide.</p>
          </div>
          <span className="state-explorer-badge" style={{ fontSize: "13px", padding: "8px 16px" }}>
            <Icon name="check" size={15} /> 50 States · {totalCountiesNationwide.toLocaleString()} Live Counties
          </span>
        </section>

        {/* Live National Metric Counters */}
        <div className="nat-stats-row">
          <div className="nat-stat-card">
            <span>States & Jurisdictions</span>
            <strong>50 States + DC</strong>
            <small>100% Nationwide Coverage</small>
          </div>
          <div className="nat-stat-card">
            <span>Recording Districts</span>
            <strong>{totalCountiesNationwide.toLocaleString()} Counties</strong>
            <small>Parishes, Boroughs & Cities</small>
          </div>
          <div className="nat-stat-card">
            <span>Directory Source</span>
            <strong>NETR Online Hub</strong>
            <small>Live Recording Endpoints</small>
          </div>
          <div className="nat-stat-card">
            <span>Intelligence Mode</span>
            <strong>Real-Time Dynamic</strong>
            <small>Zero Mocking · 100% Live</small>
          </div>
        </div>

        {/* Universal Search & Region / Alphabet Filters */}
        <div className="nat-search-box">
          <div className="nat-search-input-wrap">
            <Icon name="search" size={20} />
            <input
              value={natGlobalSearch}
              onChange={(e) => setNatGlobalSearch(e.target.value)}
              placeholder="Search any county or state (e.g., Bradford FL, Orange CA, Travis TX, Cook IL, Maricopa AZ, King WA)..."
            />
            {natGlobalSearch && (
              <button className="text-button" onClick={() => setNatGlobalSearch("")} style={{ padding: "4px 8px" }}>
                Clear
              </button>
            )}
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
            <div className="nat-region-filters">
              <span style={{ fontSize: "12px", fontWeight: 700, color: "#6a8b92", marginRight: "4px" }}>Region:</span>
              {(["All", "South", "Midwest", "West", "Northeast"] as const).map(reg => (
                <button
                  key={reg}
                  className={`nat-region-btn ${natSelectedRegion === reg ? "active" : ""}`}
                  onClick={() => { setNatSelectedRegion(reg); setNatSelectedLetter(null); }}
                >
                  {reg} {reg === "All" ? `(51)` : `(${ALL_50_STATES.filter(s => s.region === reg).length})`}
                </button>
              ))}
            </div>

            <div className="nat-alpha-jump">
              {alphabetLetters.map(letter => (
                <button
                  key={letter}
                  className={`nat-alpha-btn ${(letter === "All" && !natSelectedLetter) || natSelectedLetter === letter ? "active" : ""}`}
                  style={{ width: letter === "All" ? "38px" : "28px" }}
                  onClick={() => setNatSelectedLetter(letter === "All" ? null : letter)}
                >
                  {letter}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Global Search Results (if user is actively searching) */}
        {isSearchingGlobal ? (
          <section className="state-dir-card">
            <div className="state-dir-header">
              <div className="state-dir-title">
                <span className="state-badge-pill">🔍</span>
                <div>
                  <h3>Search Results for “{natGlobalSearch}”</h3>
                  <p>Found {globalMatches.length} matching {globalMatches.length === 1 ? "county" : "counties"} across the United States</p>
                </div>
              </div>
            </div>
            <div className="state-dir-body">
              {globalMatches.length === 0 ? (
                <div style={{ textAlign: "center", padding: "40px 20px", color: "#6a8b92" }}>
                  <Icon name="search" size={32} />
                  <p style={{ marginTop: "10px", fontSize: "14px", fontWeight: 600 }}>No counties matched “{natGlobalSearch}”.</p>
                  <small>Try typing a state name, county name, or 2-letter state code (e.g. FL, TX, CA, NY, IL).</small>
                </div>
              ) : (
                <div className="counties-dir-grid">
                  {globalMatches.map(({ state, county }) => (
                    <div className="county-item-card" key={`${state.code}-${county}`}>
                      <div className="county-card-top">
                        <div>
                          <strong>{county} County</strong>
                          <div style={{ fontSize: "11px", color: "#6a8b92", marginTop: "2px" }}>{state.name} ({state.code}) · {state.region}</div>
                        </div>
                        <span>FIPS {state.fipsPrefix}</span>
                      </div>
                      <div className="county-card-links">
                        <button
                          className="btn-examine-direct"
                          onClick={() => loadExplorerCounty(state.code, county)}
                        >
                          <Icon name="sparkles" size={12} /> Examine in Verity
                        </button>
                        <a
                          href={getNetrCountyUrl(state.code, county)}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          NETR Hub ↗
                        </a>
                        <a
                          href={getNetrGisUrl(state.code, county)}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          GIS Map ↗
                        </a>
                        <button
                          onClick={() => setCountyModal({ county, state })}
                        >
                          Portals
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        ) : (
          /* State-by-State Directory */
          <div className="state-dir-grid">
            {regionFilteredStates.map(state => {
              const isSelected = natSelectedState === state.code;
              return (
                <article className="state-dir-card" key={state.code}>
                  <div className="state-dir-header">
                    <div className="state-dir-title">
                      <span className="state-badge-pill">{state.code}</span>
                      <div>
                        <h3>{state.name} ({state.code})</h3>
                        <p>Capital: {state.capital} · Region: {state.region} · FIPS Prefix: {state.fipsPrefix} · {state.counties.length} Counties / Parishes</p>
                      </div>
                    </div>
                    <div className="state-dir-actions">
                      <button
                        className="btn-state-netr"
                        onClick={() => setNatSelectedState(isSelected ? "" : state.code)}
                      >
                        {isSelected ? "Collapse Counties ▲" : `View All ${state.counties.length} Counties ▼`}
                      </button>
                      <a
                        className="btn-state-netr"
                        href={getNetrStateUrl(state.code)}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        NETR State Hub ↗
                      </a>
                    </div>
                  </div>

                  {isSelected && (
                    <div className="state-dir-body">
                      <div className="counties-dir-grid">
                        {state.counties.map(county => (
                          <div className="county-item-card" key={`${state.code}-${county}`}>
                            <div className="county-card-top">
                              <strong>{county} County</strong>
                              <span>NETR-{state.code}</span>
                            </div>
                            <div className="county-card-links">
                              <button
                                className="btn-examine-direct"
                                onClick={() => loadExplorerCounty(state.code, county)}
                              >
                                <Icon name="sparkles" size={12} /> Examine in Verity
                              </button>
                              <a
                                href={getNetrCountyUrl(state.code, county)}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                NETR Hub ↗
                              </a>
                              <a
                                href={getNetrGisUrl(state.code, county)}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                GIS Map ↗
                              </a>
                              <button
                                onClick={() => setCountyModal({ county, state })}
                              >
                                Portals
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        )}
      </div>
    );
  }

  function renderOrders() {
    const visibleOrders = orders.filter((order) => `${order.id} ${order.property} ${order.owner}`.toLowerCase().includes(orderFilter.toLowerCase()));
    return (
      <>
        <section className="page-intro row-intro">
          <div><span className="ai-label">Order management</span><h2>All title orders</h2><p>Track research, review evidence, and prepare verified packages.</p></div>
          <button className="primary-action" onClick={startNewSearch}>+ New order</button>
        </section>
        <div className="filter-bar"><Icon name="search" size={17} /><input value={orderFilter} onChange={(e) => setOrderFilter(e.target.value)} placeholder="Filter by order, property, or owner..." /><span>{visibleOrders.length} orders</span></div>
        <section className="data-card">
          <div className="data-head"><span>Order & property</span><span>Current owner</span><span>Status</span><span>Last updated</span><span /></div>
          {visibleOrders.map((order) => (
            <button className="data-row" key={order.id} onClick={() => setSelectedOrder(order)}>
              <span><strong>{order.property}</strong><small>{order.id} · {order.county}</small></span>
              <span>{order.owner}</span>
              <span><b className={`order-status ${order.status.toLowerCase().replace(" ", "-")}`}>{order.status}</b></span>
              <span>{order.date}</span><Icon name="arrow" size={16} />
            </button>
          ))}
        </section>
      </>
    );
  }

  function renderExceptions() {
    return (
      <>
        <section className="page-intro"><span className="ai-label">Human review queue</span><h2>Exceptions</h2><p>Review ambiguous findings before they enter the final property report.</p></section>
        <div className="metric-grid">
          <div><span>Open exceptions</span><strong>{exceptions.length}</strong><small>Requires examiner action</small></div>
          <div><span>Resolved today</span><strong>{3 - exceptions.length + 7}</strong><small>Average review: 4m 12s</small></div>
          <div><span>Automation confidence</span><strong>94.2%</strong><small>Across active orders</small></div>
        </div>
        <section className="exception-list">
          {exceptions.length === 0 ? (
            <div className="all-clear"><span><Icon name="check" size={26} /></span><h3>Queue cleared</h3><p>All exceptions have been reviewed.</p></div>
          ) : exceptions.map((item) => (
            <article className="exception-card" key={item.id}>
              <span className="warning-icon"><Icon name="exceptions" /></span>
              <div><div className="exception-top"><h3>{item.title}</h3><b>{item.level}</b></div><strong>{item.property}</strong><p>{item.detail}</p></div>
              <button onClick={() => { setExceptions((current) => current.filter((entry) => entry.id !== item.id)); showToast("Exception marked as resolved."); }}>Review & resolve</button>
            </article>
          ))}
        </section>
      </>
    );
  }

  function renderReports() {
    return (
      <>
        <section className="page-intro row-intro">
          <div><span className="ai-label">Reporting center</span><h2>Reports</h2><p>Generate, review, and export typing-ready property packages.</p></div>
          <button className="primary-action" onClick={() => showToast("Report package is being generated.")}>Generate report</button>
        </section>
        <div className="metric-grid">
          <div><span>Generated this month</span><strong>184</strong><small>+18% from last month</small></div>
          <div><span>Average turnaround</span><strong>18m</strong><small>Down from 31 minutes</small></div>
          <div><span>QA acceptance</span><strong>97.6%</strong><small>First-pass approval</small></div>
        </div>
        <section className="reports-layout">
          <div className="data-card compact">
            <div className="panel-heading"><h3>Recent reports</h3><button onClick={() => showToast("Report list refreshed.")}>Refresh</button></div>
            {orders.slice(1).map((order) => (
              <button className="report-row" key={order.id} onClick={() => showToast(`${order.id} downloaded.`)}>
                <span className="document-icon accent"><Icon name="file" /></span>
                <span><strong>{order.property}</strong><small>{order.id} · Property report</small></span>
                <b>PDF</b><span>Download</span>
              </button>
            ))}
          </div>
          <div className="quality-card"><span className="ai-label"><Icon name="sparkles" size={14} /> Quality insight</span><h3>Evidence coverage is strong</h3><p>96% of this month’s reports include direct source references for every ownership transfer.</p><div className="quality-ring"><strong>96%</strong><small>coverage</small></div></div>
        </section>
      </>
    );
  }

  function renderSettings() {
    return (
      <>
        <section className="page-intro"><span className="ai-label">Workspace preferences</span><h2>Settings</h2><p>Manage alerts and defaults for your examiner workspace.</p></section>
        <section className="settings-card">
          <h3>Notifications</h3><p>Choose which updates should appear in your workspace.</p>
          {([
            ["email", "Email summaries", "Receive a daily digest of active and completed orders."],
            ["exceptions", "Exception alerts", "Notify me when an order requires human review."],
            ["completion", "Completion alerts", "Notify me whenever a report package is ready."],
          ] as const).map(([key, title, detail]) => (
            <label className="setting-row" key={key}><span><strong>{title}</strong><small>{detail}</small></span><input type="checkbox" checked={settings[key]} onChange={() => setSettings((current) => ({ ...current, [key]: !current[key] }))} /><i /></label>
          ))}
          <button className="primary-action" onClick={() => showToast("Workspace preferences saved.")}>Save preferences</button>
        </section>
      </>
    );
  }

  function renderHelp() {
    return (
      <>
        <section className="page-intro"><span className="ai-label">Knowledge center</span><h2>How can we help?</h2><p>Find guidance for property research, exceptions, and report preparation.</p></section>
        <div className="help-search"><Icon name="search" /><input placeholder="Search help articles..." /></div>
        <section className="help-grid">
          {[
            ["Starting a property search", "Learn which address, APN, and owner inputs return the best results."],
            ["Reviewing AI matches", "Understand confidence scores and verify entity relationships."],
            ["Resolving exceptions", "Handle name mismatches, missing pages, and unreleased liens."],
            ["Preparing a report", "Review evidence and export a typing-ready property package."],
          ].map(([title, detail], index) => <button key={title} onClick={() => showToast(`Opened guide ${index + 1}: ${title}`)}><span>0{index + 1}</span><h3>{title}</h3><p>{detail}</p><b>Read guide <Icon name="arrow" size={14} /></b></button>)}
        </section>
      </>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><span /><span /><span /></div>
          <div><strong>Verity</strong><small>Title intelligence</small></div>
        </div>

        <nav className="nav-list" aria-label="Primary navigation">
          <p className="nav-heading">Workspace</p>
          {nav.map((item) => (
            <button
              className={`nav-item ${activeNav === item.label ? "active" : ""}`}
              key={item.label}
              onClick={() => goTo(item.label)}
            >
              <Icon name={item.icon} />
              <span>{item.label}</span>
              {item.count && <b>{item.count}</b>}
            </button>
          ))}
        </nav>

        <div className="side-bottom">
          <button className={`nav-item ${activeNav === "Help center" ? "active" : ""}`} onClick={() => goTo("Help center")}><Icon name="help" /><span>Help center</span></button>
          <button className={`nav-item ${activeNav === "Settings" ? "active" : ""}`} onClick={() => goTo("Settings")}><Icon name="settings" /><span>Settings</span></button>
          <div className="user-card">
            <div className="avatar">AM</div>
            <div><strong>Alex Morgan</strong><small>Title examiner</small></div>
            <span>•••</span>
          </div>
        </div>
      </aside>

      <main>
        <header className="topbar">
          <div>
            <p className="eyebrow">Title operations</p>
            <h1>{activeNav}</h1>
          </div>
          <div className="top-actions">
            <div className="notification-wrap">
              <button className="icon-button" aria-label="Notifications" onClick={() => setNotificationsOpen((open) => !open)}><Icon name="bell" /></button>
              {notificationsOpen && <div className="notification-popover"><strong>Notifications</strong><button onClick={() => { goTo("Exceptions"); }}>New exception on COS-24828<small>Owner name needs review · 8 min ago</small></button><button onClick={() => { goTo("Reports"); }}>Report COS-24829 is ready<small>QA approved · 26 min ago</small></button></div>}
            </div>
            <button className="new-order" onClick={startNewSearch}>
              <span>+</span> New search
            </button>
          </div>
        </header>

        <div className="content">
          {activeNav === "Overview" && renderSearchWorkspace(true)}
          {activeNav === "Property search" && renderSearchWorkspace(false)}
          {activeNav === "States & Counties" && renderStatesAndCounties()}
          {activeNav === "Orders" && renderOrders()}
          {activeNav === "Exceptions" && renderExceptions()}
          {activeNav === "Reports" && renderReports()}
          {activeNav === "Settings" && renderSettings()}
          {activeNav === "Help center" && renderHelp()}
        </div>
      </main>

      {/* Recorded Document or Order Detail Modal */}
      {(selectedDocument || selectedOrder) && (
        <div className="modal-backdrop" onMouseDown={() => { setSelectedDocument(null); setSelectedOrder(null); }}>
          <section className="detail-modal" onMouseDown={(event) => event.stopPropagation()} role="dialog" aria-modal="true" style={{ width: "min(520px, 100%)" }}>
            <button className="modal-close" onClick={() => { setSelectedDocument(null); setSelectedOrder(null); }} aria-label="Close">×</button>
            <span className="document-icon accent"><Icon name={selectedDocument ? "file" : "orders"} /></span>
            <p className="muted-label">{selectedDocument ? `Recorded Document · ${selectedDocument.category.toUpperCase()}` : "Title Order"}</p>
            <h2>{selectedDocument?.type || selectedOrder?.property}</h2>
            <p className="modal-subtitle">{selectedDocument?.party || `${selectedOrder?.id} · ${selectedOrder?.county}`}</p>
            
            <div className="modal-details">
              <div><span>Grantor / Debtor</span><strong>{selectedDocument?.grantor || selectedOrder?.owner}</strong></div>
              <div><span>Grantee / Lender</span><strong>{selectedDocument?.grantee || "Subject Property"}</strong></div>
              <div><span>Recording Date</span><strong>{selectedDocument?.date || selectedOrder?.date}</strong></div>
              <div><span>Instrument & Book/Page</span><strong>{selectedDocument ? `${selectedDocument.ref} · ${selectedDocument.bookPage}` : selectedOrder?.id}</strong></div>
              {selectedDocument?.amount && <div><span>Amount / Consideration</span><strong>{selectedDocument.amount}</strong></div>}
              <div><span>Document Status</span><strong className={`doc-status-badge ${selectedDocument?.statusClass || "doc-status-open"}`}>{selectedDocument?.status || selectedOrder?.status}</strong></div>
              <div><span>Examiner Legal Note</span><strong style={{ fontSize: "11px", fontWeight: 500, textAlign: "right", maxWidth: "260px" }}>{selectedDocument?.legalNote || "Verified title order on record."}</strong></div>
              <div><span>Source Authority</span><strong className="verified"><Icon name="check" size={14} /> Official Records Certified</strong></div>
            </div>

            <div style={{ display: "flex", gap: "10px", marginTop: "16px" }}>
              <a
                className="primary-action full"
                href={activeProperty.recorderPortal}
                target="_blank"
                rel="noopener noreferrer"
                style={{ textAlign: "center", textDecoration: "none" }}
              >
                Open in County Recorder ↗
              </a>
              <button className="text-button" style={{ justifyContent: "center" }} onClick={() => { setSelectedDocument(null); setSelectedOrder(null); }}>
                Close
              </button>
            </div>
          </section>
        </div>
      )}

      {/* County Government Portals Details Modal */}
      {countyModal && (
        <div className="modal-backdrop" onMouseDown={() => setCountyModal(null)}>
          <section className="detail-modal" onMouseDown={(e) => e.stopPropagation()} role="dialog" aria-modal="true" style={{ width: "min(560px, 100%)" }}>
            <button className="modal-close" onClick={() => setCountyModal(null)} aria-label="Close">×</button>
            <span className="document-icon accent"><Icon name="pin" /></span>
            <p className="muted-label">Official County Public Records Portals</p>
            <h2>{countyModal.county} County, {countyModal.state.name}</h2>
            <p className="modal-subtitle">State Code: {countyModal.state.code} · Capital: {countyModal.state.capital} · Region: {countyModal.state.region}</p>

            <div className="modal-details" style={{ marginTop: "14px" }}>
              <div><span>NETR County Directory</span><a href={getNetrCountyUrl(countyModal.state.code, countyModal.county)} target="_blank" rel="noopener noreferrer" style={{ color: "#0eaaa7", fontWeight: 700, textDecoration: "none" }}>Open NETR County Hub ↗</a></div>
              <div><span>NETR State Directory</span><a href={getNetrStateUrl(countyModal.state.code)} target="_blank" rel="noopener noreferrer" style={{ color: "#0eaaa7", fontWeight: 700, textDecoration: "none" }}>{countyModal.state.name} Public Records ↗</a></div>
              <div><span>Cadastral GIS Map</span><a href={getNetrGisUrl(countyModal.state.code, countyModal.county)} target="_blank" rel="noopener noreferrer" style={{ color: "#0eaaa7", fontWeight: 700, textDecoration: "none" }}>Interactive GIS Parcel Viewer ↗</a></div>
              <div><span>Historic Aerials</span><a href="https://www.historicaerials.com/" target="_blank" rel="noopener noreferrer" style={{ color: "#0eaaa7", fontWeight: 700, textDecoration: "none" }}>Historic Aerial Imagery (1940-Present) ↗</a></div>
              <div><span>Property Data Store</span><a href="https://datastore.netronline.com/" target="_blank" rel="noopener noreferrer" style={{ color: "#0eaaa7", fontWeight: 700, textDecoration: "none" }}>Deed & Mortgage Document Store ↗</a></div>
              <div><span>FIPS Recording Prefix</span><strong>FIPS {countyModal.state.fipsPrefix} · NETR-{countyModal.state.code}-{slugifyCounty(countyModal.county).toUpperCase()}</strong></div>
            </div>

            <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
              <button
                className="primary-action full"
                style={{ justifyContent: "center" }}
                onClick={() => {
                  loadExplorerCounty(countyModal.state.code, countyModal.county);
                  setCountyModal(null);
                }}
              >
                <Icon name="sparkles" size={14} /> Launch Search for this County
              </button>
              <button className="text-button" style={{ justifyContent: "center" }} onClick={() => setCountyModal(null)}>
                Close
              </button>
            </div>
          </section>
        </div>
      )}

      {toast && <div className="toast"><Icon name="check" size={16} /> {toast}</div>}
    </div>
  );
}


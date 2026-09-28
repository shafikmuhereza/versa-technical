"""
build_site.py - generates every HTML page of the A5 Systems Uganda website.

HOW TO USE
    python3 tools/build_site.py        (run from the website folder; needs Python 3, no extra packages)

WHY A SCRIPT?
    Every page shares the same header, menu, footer, and search-engine (SEO) markup.
    Keeping that in ONE place means a change (for example a new phone number) is made once
    and applied to all pages, instead of editing 25 files by hand.

WHAT TO EDIT (all near the top of this file)
    1. Site-wide constants ........ phone, email, address, site URL  (SITE, PHONE, EMAIL, ADDRESS)
    2. NAV ........................ the main menu links
    3. S  (core services) ......... one entry per service page: wording, SEO title/description, FAQs, photos
    4. S2 (specialist services) ... same format, listed under "More ways we can help"
    5. HOME / ABOUT / CONTACT ..... the page-specific sections further down (search for the big "# ====" banners)

IMPORTANT
    Running the script OVERWRITES the generated .html files, sitemap.xml and robots.txt.
    If you prefer to edit the .html files by hand, stop using this script (or copy your edits into it).
    Styles live in styles.css, icons in icons.svg, pictures in images/.
"""
import json, os, html

# The website folder is the parent of the folder that contains this script (tools/..)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------------------------------------------
# 1. SITE-WIDE CONSTANTS - change contact details here, then re-run the script
# ---------------------------------------------------------------------------
SITE = "https://afive.cc"
PHONE = "+256757732991"
PHONE_DISPLAY = "+256 757 732 991"
EMAIL = "sales@afive.cc"
TODAY = "2026-09-28"
ADSENSE = '<!-- Google AdSense advertising script (loads ads; remove this line to stop ads) -->\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9204998406606528" crossorigin="anonymous"></script>'
# Bing Webmaster Tools ownership check (keep it, or Bing can no longer verify the site)
BING = '<meta name="msvalidate.01" content="171C2F4F23F156D2AF89DA9D40F13F31">'
ADDRESS = "Kitende A, Kajjansi T/C, Wakiso District, Uganda"

def ic(name, cls="icon"):
    """Return an inline icon. `name` must exist as a <symbol id=...> in icons.svg."""
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="icons.svg#{name}"/></svg>'

# ---------------------------------------------------------------------------
# 2. MAIN MENU - (label, file). The order here is the order in the header.
#    "Get a Quote" is added separately as the highlighted button (see header()).
# ---------------------------------------------------------------------------
NAV = [("Home","index.html"),("Services","services.html"),("Products","products.html"),("IoT Monitoring","Monitoring.html"),("About","about.html"),("Contact","contact.html")]

# The four-step "how we work" process, reused on the home, services, about and service pages
STEPS = [("Diagnose","We trace the fault to its cause, so you know exactly what is wrong before any money is spent."),
         ("Repair or upgrade","We repair the failed part, or upgrade legacy systems that are past their best."),
         ("Install and commission","New equipment is installed, tested under real conditions and handed over working."),
         ("Support","Unmatched technical support after handover, with maintenance plans to keep things running.")]

# ------------------------------------------------------------------ service pages
S = {}
# ---------------------------------------------------------------------------
# 3. CORE SERVICE PAGES  (each entry below becomes one page)
#    Field guide:
#      nav / card / blurb ... label in menus and footer / card heading / card text
#      icon .................. icon name from icons.svg
#      title / desc .......... SEO: text Google shows in results (title ~60, desc ~155 characters)
#      h1 / intro ............ heading and opening paragraph at the top of the page
#      do_title / do ......... "what we do" heading and bullet list
#      signs_title / signs ... "signs you need us" heading and bullet list
#      photo ................. main picture (file in images/, width, height, alt text, caption)
#      strip ................. optional row of extra photos under the main section
#      faq ................... question/answer pairs; ALSO used for Google's FAQ rich results
#      related ............... other pages to link to at the bottom
# ---------------------------------------------------------------------------
S = {}
S["ups-repair-uganda.html"] = dict(
 nav="UPS Repair & Maintenance", icon="zap", card="UPS repair, installation and maintenance",
 blurb="All brands of UPS systems and inverters, installed, repaired and maintained, with component-level power electronics repair.",
 title="UPS Repair & Maintenance in Uganda | A5 Systems",
 desc="UPS repair, installation and maintenance in Uganda for all brands of UPS, inverters and power electronics. Call A5 Systems Uganda.",
 h1="UPS Repair, Installation & Maintenance in Uganda",
 intro="A5 Systems Uganda installs, repairs and maintains all brands of UPS systems and inverters. Our expertise extends to all power electronics devices, so faults are traced to the failing component instead of replacing whole units unnecessarily.",
 do_title="What we do for your UPS",
 do=["UPS and inverter installation and commissioning","Fault diagnosis and component-level repair","Repair of rectifiers, boost converters and other power electronics","Battery bank testing, replacement and maintenance","Preventive maintenance contracts to reduce unexpected downtime","Supply of IGBT modules, thyristors, power diodes, capacitors and cooling fans"],
 signs_title="Signs your UPS needs attention",
 signs=["Alarm, beeping or a fault light that will not clear","Battery runtime is much shorter than it used to be","Overheating, loud fans or a burning smell","The UPS switches to bypass or shuts down when the load increases","Swollen, leaking or very old batteries"],
 photo=("img4-photo.webp",900,675,"UPS cabinets with battery banks in an equipment room","UPS cabinets and battery banks"),
 faq=[("Which UPS brands do you service?","We work on all brands of UPS systems and inverters. Send us the make and model and a photo of the nameplate and we will advise on repair or replacement."),
      ("Is it better to repair or replace a faulty UPS?","Often a repair is the more economical choice, but not always. We diagnose first, then tell you what is wrong and what each option involves so you can decide."),
      ("Do you offer maintenance contracts?","Yes. We offer maintenance contracting so your UPS and battery banks are inspected and tested on a regular schedule.")],
 related=["generator-maintenance-uganda.html","energy-storage-solutions-uganda.html","Monitoring.html"])
S["generator-maintenance-uganda.html"] = dict(
 nav="Generator Maintenance", icon="cog", card="Generator maintenance and repair",
 blurb="Generators of all sizes serviced and repaired: preventive maintenance, fault diagnosis, overhaul, spares and remote monitoring.",
 title="Generator Maintenance & Repair in Uganda | A5 Systems",
 desc="Generator servicing, repair, spares and remote monitoring in Uganda. Preventive maintenance, fault diagnosis and overhaul by A5 Systems Uganda.",
 h1="Generator Maintenance & Repair in Uganda",
 intro="We service and repair generators of all sizes, from small standby units to large industrial sets. A well-maintained generator starts when you need it and keeps your operation running through power cuts.",
 do_title="Generator services",
 do=["Preventive maintenance and routine servicing","Fault diagnosis and repair","Overhaul services","Generator spares supply","Installation of generator monitoring systems","Standby support services"],
 signs_title="Signs your generator needs service",
 signs=["Hard starting, or it fails to start","Black or white smoke, or unusual exhaust","Low oil pressure or overheating","It struggles to pick up load, or the frequency or voltage is unstable","It has been a long time since the last service"],
 extra='<p>Our <a href="Monitoring.html">remote monitoring</a> lets owners and facility managers see generator status and alarms from anywhere, so faults are caught early and servicing is planned instead of reactive.</p>',
 faq=[("How often should a generator be serviced?","Follow the manufacturer's schedule, which is normally based on running hours or elapsed time. We can set up a service plan for your set and keep records of each visit."),
      ("Can you monitor a generator remotely?","Yes. We install monitoring systems that give real-time visibility of generator condition and send alerts."),
      ("Do you supply spare parts?","Yes, we supply generator spares alongside servicing and repair.")],
 related=["ups-repair-uganda.html","air-compressor-services-uganda.html","Monitoring.html"])
S["solar-installation-uganda.html"] = dict(
 nav="Solar Installation", icon="sun", card="Solar installation, maintenance and repair",
 blurb="Complete solar systems for homes, businesses and farms, plus troubleshooting, repairs, cleaning and monitoring.",
 title="Solar Installation & Repair in Uganda | A5 Systems",
 desc="Solar system design, installation, repair and monitoring in Uganda for homes, businesses and farms, with hybrid inverters and battery storage.",
 h1="Solar Installation, Repair & Monitoring in Uganda",
 intro="We design and install complete solar systems for homes, businesses and farms, and our team also handles troubleshooting, repairs and upgrades of systems that are already installed.",
 do_title="Solar and hybrid services",
 do=["Solar system design and installation","Hybrid inverters and grid integration","Battery banks for backup and off-grid use","Troubleshooting, repairs and upgrades","Panel cleaning and maintenance","Remote solar monitoring for performance data and fault alerts"],
 signs_title="Signs your solar system needs a check",
 signs=["Less energy than before, or than you expected","The inverter shows fault codes or keeps restarting","Batteries do not last through the night","You want to add batteries, more panels or a hybrid inverter","Dirty or shaded panels"],
 extra='<p>Remote monitoring shows real-time performance and energy yield and alerts you to faults, so underperforming systems are found quickly. See our <a href="Monitoring.html">IoT monitoring</a> page.</p>',
 faq=[("Do you install battery storage?","Yes. We provide battery systems for backup and off-grid use, including lithium, AGM and gel batteries, integrated with solar and grid supply."),
      ("Can you repair an existing solar system?","Yes. We troubleshoot, repair and upgrade existing installations, including monitoring installation."),
      ("Can I monitor my solar system from my phone?","Yes. Remote solar monitoring gives you performance data and fault alerts wherever you are.")],
 related=["energy-storage-solutions-uganda.html","building-management-systems-uganda.html","Monitoring.html"])
S["building-management-systems-uganda.html"] = dict(
 nav="Building Management Systems", icon="building", card="Building management systems (BMS)",
 blurb="One place to control and monitor HVAC, lighting, power and energy, with integration and optimization.",
 title="Building Management Systems (BMS) Uganda | A5 Systems",
 desc="Building management system (BMS) design, integration and energy management in Uganda: HVAC, lighting, power and monitoring. A5 Systems Uganda.",
 h1="Building Management Systems (BMS) in Uganda",
 intro="We design, integrate and commission building management systems that give owners and facility managers centralized control and visibility over HVAC, lighting, power and other building services.",
 do_title="BMS and energy management",
 do=["Building automation for HVAC, security and energy systems","Lighting control with scheduling and remote management","Energy management and optimization","Integration with UPS, generators, solar and other plant","Dashboards, gateways, data acquisition and control modules","BMS solutions including ABB BuildingPro"],
 signs_title="When a BMS makes sense",
 signs=["Energy bills are high and you cannot see where the energy goes","Air conditioning and lighting run when nobody needs them","Equipment faults are found only after something stops","You manage several buildings or sites and want one view","You are adding or upgrading plant and want it all integrated"],
 extra='<p>Our <a href="Monitoring.html">IoT and asset monitoring</a> extends visibility across buildings and equipment.</p>',
 faq=[("What can a BMS control?","Typically HVAC, lighting, power and monitoring points. We scope the system to your building and equipment."),
      ("Can you add monitoring to an existing building?","Yes. Sensors, gateways and dashboards can often be added to existing plant without replacing it."),
      ("What do we get from a BMS?","Comfort, energy savings and centralized control, plus the data to plan maintenance instead of reacting to failures.")],
 related=["air-conditioning-services-uganda.html","lighting-solutions-uganda.html","Monitoring.html"])
S["air-conditioning-services-uganda.html"] = dict(
 nav="Air Conditioning", icon="snow", card="Air conditioning systems",
 blurb="Installation, maintenance and repair of split, window, cassette, VRF/VRV and packaged units, homes to industry.",
 title="Air Conditioning Installation & Repair Uganda | A5",
 desc="Air conditioning installation, maintenance and repair in Uganda: split, cassette, VRF/VRV and packaged units for homes, offices and industry.",
 h1="Air Conditioning Installation, Maintenance & Repair in Uganda",
 intro="We install, maintain and repair residential, commercial and industrial air conditioning systems. Our expertise covers split ACs, window units, ceiling cassette systems, VRF/VRV systems and packaged central units.",
 do_title="Systems we handle",
 do=["Split air conditioners and window units","Ceiling cassette systems","VRF/VRV systems","Packaged central units","Refrigeration and cooling system repairs and maintenance","Chillers, pumps and cooling towers"],
 signs_title="Signs your AC needs attention",
 signs=["It runs but does not cool properly","Water leaks from the indoor unit","Unusual noises, smells or vibration","Ice forming on pipes or the indoor unit","Rising electricity bills with no change in use"],
 faq=[("Do you do maintenance as well as repairs?","Yes. We provide installation, routine maintenance and repair."),
      ("Do you work on commercial and industrial systems?","Yes. We handle residential, commercial and industrial systems, including VRF/VRV and packaged units."),
      ("Can air conditioning be connected to a BMS?","Yes. Where the equipment allows, we can bring it into a building management system for scheduling and monitoring.")],
 related=["building-management-systems-uganda.html","industrial-automation-uganda.html","Monitoring.html"])
S["industrial-automation-uganda.html"] = dict(
 nav="Industrial Automation & Repair", icon="factory", card="Industrial automation and equipment repair",
 blurb="PLCs, drives, motor controllers, instrumentation and industrial wiring: troubleshooting, repair, maintenance and installation.",
 title="Industrial Automation & Equipment Repair Uganda | A5",
 desc="Industrial automation, PLCs, VFD and drive repair, motor controllers and industrial electrical services in Uganda. A5 Systems Uganda.",
 h1="Industrial Automation & Equipment Repair in Uganda",
 intro="We support industry with tailored technical services: troubleshooting and repairing complex systems, maintaining and installing advanced technologies, and upgrading legacy equipment.",
 do_title="Automation, controls and repair",
 do=["PLCs, IO solutions and industrial instrumentation","Variable frequency drives and motor controllers","Rectifiers, boost converters and power electronics repair","Sensors and general industrial wiring","Pumps, chillers and cooling towers","Upgrades of legacy control systems"],
 signs_title="When to call us",
 signs=["A drive, controller or PLC has tripped or failed","A machine stops without a clear cause","Legacy control equipment is unreliable or hard to get parts for","You want to automate a manual process","You need reliable industrial wiring or instrumentation"],
 photo=("img8-photo.webp",600,800,"Power module and busbar connections inside an industrial cabinet","Power electronics inside an industrial cabinet"),
 faq=[("Can you repair VFDs and drives?","Yes. We repair variable frequency drives, motor controllers, rectifiers and related power electronics."),
      ("Can you upgrade an old control system?","Yes. We diagnose complex faults, upgrade legacy systems and commission the new equipment."),
      ("Do you offer maintenance contracts?","Yes. We offer maintenance contracting for industrial and utility equipment.")],
 related=["air-compressor-services-uganda.html","embedded-systems-prototyping-uganda.html","ups-repair-uganda.html"])
S["air-compressor-services-uganda.html"] = dict(
 nav="Air Compressor Services", icon="gauge", card="Air compressor technical services",
 blurb="Repairs, maintenance and installation of industrial air compressors, and air monitoring systems.",
 title="Air Compressor Repair & Maintenance Uganda | A5",
 desc="Industrial air compressor repair, maintenance and installation in Uganda, including air monitoring systems. A5 Systems Uganda.",
 h1="Air Compressor Repair, Maintenance & Installation in Uganda",
 intro="Compressed air runs tools, packaging lines and processes, so a failing compressor stops production. We provide repairs, maintenance and installation for industrial air compressors, and air monitoring systems.",
 do_title="Compressor services",
 do=["Air compressor repair and fault diagnosis","Routine and preventive maintenance","Installation and commissioning","Air monitoring systems","Maintenance contracts","Support for related equipment such as motors, drives and controls"],
 signs_title="Signs your compressor needs attention",
 signs=["Pressure builds slowly or will not reach the set point","Overheating or frequent shutdowns","Oil in the air lines or unusual oil consumption","The compressor cycles on and off too often","Rising electricity use for the same output"],
 faq=[("Do you install new compressors?","Yes. We provide installation and commissioning as well as repairs and maintenance."),
      ("What is an air monitoring system?","It tracks how your compressed air system is performing so problems are noticed early. See our IoT monitoring page for how monitoring works."),
      ("Can you maintain our compressors under a contract?","Yes. Maintenance contracting is available for compressors and other industrial utility equipment.")],
 related=["industrial-automation-uganda.html","generator-maintenance-uganda.html","Monitoring.html"])
S["energy-storage-solutions-uganda.html"] = dict(
 nav="Energy Storage", icon="battery", card="Energy storage solutions",
 blurb="Lithium, AGM and gel battery systems for backup and off-grid power, integrated with solar and grid.",
 title="Energy Storage & Battery Systems Uganda | A5 Systems",
 desc="Battery banks and energy storage in Uganda: lithium, AGM and gel batteries for backup and off-grid power, with hybrid solar integration.",
 h1="Energy Storage & Battery Systems in Uganda",
 intro="We provide advanced battery systems for backup power and off-grid use, including lithium, AGM and gel batteries. Solutions include battery banks, battery management systems and hybrid integration with solar and grid supply.",
 do_title="Energy storage services",
 do=["Battery bank design and installation","Lithium, AGM and gel battery options","Battery management systems (BMS)","Hybrid integration with solar and grid","Backup power for homes, businesses and industry","Battery testing and replacement"],
 signs_title="Choosing a battery type",
 signs=["Lithium batteries usually cost more up front but are lighter and last longer","AGM and gel batteries are sealed lead-acid types with a lower purchase price","The right size depends on your load and how long you need to run on batteries","We recommend a type after understanding your load and budget"],
 faq=[("Which battery is best for solar?","It depends on your load, budget and how often the batteries will be cycled. Tell us what you want to run and for how long and we will recommend a solution."),
      ("Can you add batteries to my existing solar system?","In many cases yes, depending on your inverter. We can assess it and advise on hybrid integration."),
      ("Do you replace old battery banks?","Yes. We test, maintain and replace battery banks for UPS and solar systems.")],
 related=["solar-installation-uganda.html","ups-repair-uganda.html","Monitoring.html"])
S["lighting-solutions-uganda.html"] = dict(
 nav="Lighting Solutions", icon="bulb", card="Lighting solutions",
 blurb="Street, residential, commercial and industrial lighting: supply, installation, repair, maintenance and control.",
 title="Lighting Installation & Repair in Uganda | A5 Systems",
 desc="Street, commercial, industrial and residential lighting in Uganda: supply, installation, repair, LED driver repair and lighting control.",
 h1="Lighting Installation, Repair & Control in Uganda",
 intro="We provide expert lighting solutions for streets, residential, commercial and industrial spaces. We supply, install, repair and maintain, and we can add smart control for scheduling and remote management.",
 do_title="Lighting services",
 do=["Supply and installation of lighting","Street, garden, commercial and industrial lighting","Repair and maintenance of fittings","LED driver repair","Lighting control systems with scheduling","Remote lighting management"],
 signs_title="Why upgrade your lighting",
 signs=["Old fittings are costly to run and fail often","Outdoor areas need reliable, automatic lighting","You want lights that switch on a schedule or by sensor","LED drivers keep failing"],
 photo=("lighting.webp",709,398,"Garden lighting at night","Outdoor lighting"),
 faq=[("Can you repair LED lights and drivers?","Yes. We repair LED lights and LED drivers as well as supplying and installing new fittings."),
      ("Can lighting be controlled automatically?","Yes. Lighting control systems provide scheduling, smart sensors and remote management."),
      ("Do you light large outdoor areas and streets?","Yes. We handle street, residential, commercial and industrial lighting.")],
 related=["building-management-systems-uganda.html","solar-installation-uganda.html","Monitoring.html"])
S["embedded-systems-prototyping-uganda.html"] = dict(
 nav="Embedded Systems & Prototyping", icon="chip", card="Prototyping and custom embedded systems",
 blurb="From concept to working prototype: custom controllers and embedded systems designed and built for your needs.",
 title="Embedded Systems & Prototyping Uganda | A5 Systems",
 desc="Custom embedded systems, controllers and electronics prototyping in Uganda: design, programming and testing from concept to working prototype.",
 h1="Embedded Systems Design & Prototyping in Uganda",
 intro="Need a device that does not exist yet? We provide end-to-end development from concept to functional prototype. We design and build innovative embedded systems tailored to your needs.",
 do_title="What we build",
 do=["Custom controllers and application-specific electronics","Embedded systems design and programming","Circuit design and prototype boards","Testing and refinement of custom solutions","Connected devices that report data to dashboards","Integration with sensors, PLCs and existing equipment"],
 signs_title="A good fit if you",
 signs=["Have an idea for a control or monitoring device and need a working prototype","Need a controller made for one specific process","Want to add sensing or connectivity to existing equipment","Need help testing and improving an existing design"],
 photo=("img7-photo.webp",790,800,"Prototype circuit board with a microcontroller","A prototype electronics board"),
 faq=[("Can you build a one-off prototype?","Yes. We take an idea from concept to a functional prototype, and test it."),
      ("Can you connect a device to the internet?","Yes. We build connected devices that send data to dashboards and alerts. See our IoT monitoring page."),
      ("Do you program the device too?","Yes. Embedded design and programming are both part of the service.")],
 related=["industrial-automation-uganda.html","Monitoring.html","building-management-systems-uganda.html"])
SERVICE_ORDER = list(S.keys())

def P(name,alt,cap,portrait=False):
    """Photo tuple for images/work-<name>.webp (real project photo). portrait=True for 4:5 pictures."""
    return (f"work-{name}.webp", 800 if portrait else 1000, 1000 if portrait else 750, alt, cap)
S["ups-repair-uganda.html"]["photo"]=P("ups-room","Installed UPS cabinets and battery banks in an equipment room","UPS installation and commissioning")
S["ups-repair-uganda.html"]["strip"]=[P("ups-battery-test","Technician testing UPS battery terminals with a battery tester","Testing UPS battery banks"),P("ups-internals","Open UPS cabinet showing power and control boards","Inside a UPS: power and control boards"),P("ups-row","A row of standalone UPS units","Standalone UPS units")]
S["generator-maintenance-uganda.html"]["photo"]=P("gen-service","Technician carrying out scheduled maintenance on a standby generator","Generator maintenance and servicing")
S["generator-maintenance-uganda.html"]["strip"]=[P("gen-laptop","Engineer diagnosing a generator controller with a laptop","Diagnosing a generator controller with a laptop"),P("gen-hardhats","Technicians working inside a generator enclosure","Servicing a generator inside its canopy"),P("gen-canopy","A canopy-enclosed standby generator","A canopy-enclosed standby generator")]
S["air-conditioning-services-uganda.html"]["photo"]=P("ac-service","Technician on a ladder servicing a wall-mounted air conditioner","Servicing a wall-mounted air conditioner")
S["industrial-automation-uganda.html"]["photo"]=P("cabinet-vfd","Control cabinet with a drive, controller board and protection devices","A drive and control cabinet")
S["industrial-automation-uganda.html"]["strip"]=[P("cabinet-panel","Wiring inside an industrial control panel","Control panel wiring"),P("cabinet-contactors","Contactors and circuit protection in a control panel","Contactors and protection devices"),("img8-photo.webp",600,800,"Power module and busbar connections inside an industrial cabinet","Power electronics inside a cabinet")]
S["energy-storage-solutions-uganda.html"]["photo"]=P("batteries","Industrial nickel-cadmium battery cells","Industrial nickel-cadmium batteries",True)
S["energy-storage-solutions-uganda.html"]["strip"]=[P("ups-battery-test","Technician testing battery terminals with a battery tester","Testing a battery bank"),P("ups-room","Battery banks on stands beside UPS cabinets","Battery banks on stands")]
S["embedded-systems-prototyping-uganda.html"]["strip"]=[P("board-mcu","Microcontroller on a circuit board","Microcontroller on a circuit board"),P("ups-board","Power electronics board with capacitors and connectors","Power electronics board")]
S["building-management-systems-uganda.html"]["photo"]=P("team-site","A5 Systems team inspecting an electrical cabinet on site","On a site visit to an electrical cabinet")

# ---- Vector illustrations used where we have no photo (solar, compressor, cooling).
#      Shown as graphic only. Files: images/illus-*.svg (each SVG is commented section by section).
def IL(f,w,h,alt,cap):
    """GRAPHIC-ONLY picture (vector illustration). The caption argument is ignored on purpose:
    illustrations are shown without any caption text."""
    return (f,w,h,alt,"")
S["solar-installation-uganda.html"]["photo"]=IL("illus-solar.svg",800,600,"Illustration of a house with solar panels on the roof, an inverter and a battery unit","a solar system with inverter and battery storage")
S["air-compressor-services-uganda.html"]["photo"]=IL("illus-compressor.svg",800,600,"Illustration of an industrial air compressor with tank, motor, pressure gauge and control panel","an industrial air compressor")

# ---- search-focused titles and descriptions (location terms included)
# Search-engine titles/descriptions for the core service pages (kept together for easy review).
# They override the title/desc written inside each S[...] entry above.
SEO = {
"ups-repair-uganda.html":("UPS Repair & Maintenance in Kampala, Uganda | A5 Systems","UPS repair, installation and maintenance in Kampala and across Uganda for all brands of UPS, inverters and power electronics. Call A5 Systems."),
"generator-maintenance-uganda.html":("Generator Maintenance & Repair Kampala, Uganda | A5","Generator servicing, repair, spares and remote monitoring in Kampala, Wakiso and across Uganda. Preventive maintenance and overhaul by A5 Systems."),
"solar-installation-uganda.html":("Solar Installation & Repair in Kampala, Uganda | A5","Solar system design, installation, repair and monitoring in Kampala and across Uganda for homes, businesses and farms, with hybrid inverters and batteries."),
"building-management-systems-uganda.html":("Building Management Systems Kampala, Uganda | A5","Building management system (BMS) design, integration and energy management in Kampala and Uganda: HVAC, lighting, power and monitoring."),
"air-conditioning-services-uganda.html":("Air Conditioning Installation & Repair Kampala | A5","Air conditioning installation, maintenance and repair in Kampala and across Uganda: split, cassette, VRF/VRV and packaged units for homes and industry."),
"industrial-automation-uganda.html":("Industrial Automation & Repair in Uganda | A5 Systems","Industrial automation, PLCs, VFD and drive repair and industrial electrical services in Kampala and across Uganda. A5 Systems Uganda."),
"air-compressor-services-uganda.html":("Air Compressor Repair & Maintenance Kampala | A5","Industrial air compressor repair, maintenance and installation in Kampala and across Uganda, including air monitoring systems. A5 Systems Uganda."),
"energy-storage-solutions-uganda.html":("Battery & Energy Storage Systems Kampala, Uganda | A5","Battery banks and energy storage in Kampala and across Uganda: lithium, AGM and gel batteries for backup and off-grid power, with solar integration."),
"lighting-solutions-uganda.html":("Lighting Installation & Repair Kampala, Uganda | A5","Street, commercial, industrial and residential lighting in Kampala and across Uganda: supply, installation, LED driver repair and lighting control."),
"embedded-systems-prototyping-uganda.html":("Embedded Systems & Prototyping Uganda | A5 Systems","Custom embedded systems, controllers and electronics prototyping in Uganda: design, programming and testing from concept to working prototype."),
}
for k,(t,d) in SEO.items(): S[k]["title"]=t; S[k]["desc"]=d

# ---------------------------------------------------------------------------
# 4. SPECIALIST SERVICE PAGES - same fields as the core services above.
#    Shown under "More ways we can help" on services.html and in the home page link row.
# ---------------------------------------------------------------------------
S2 = {}
S2["vfd-motor-controller-repair-uganda.html"] = dict(
 nav="VFD & Motor Controller Repair", icon="cog", card="VFD and motor controller repair",
 blurb="Fault diagnosis and repair of variable frequency drives and motor controllers, with IGBT modules, capacitors and fans supplied.",
 title="VFD & Drive Repair in Kampala, Uganda | A5 Systems",
 desc="Variable frequency drive (VFD) and motor controller repair in Kampala and across Uganda. Fault diagnosis, IGBT module replacement and commissioning.",
 h1="VFD & Motor Controller Repair in Uganda",
 intro="When a variable frequency drive or motor controller fails, the machine it runs stops. We diagnose the fault, repair the drive at component level and commission it, so production gets going again.",
 do_title="Drive and motor controller services",
 do=["Fault diagnosis on variable frequency drives and motor controllers","Repair of power stages: IGBT modules, rectifiers and diodes","Replacement of DC bus capacitors and cooling fans","Commissioning and setup after repair","Supply of IGBT modules, thyristors, capacitors and cooling fans","Advice on repair versus replacement"],
 signs_title="Signs a drive needs repair",
 signs=["The drive trips on overcurrent, overvoltage or over-temperature","The display is dead or the drive will not start","The motor runs roughly or cannot reach speed","Faults keep returning after a reset","Burning smell, blown fuses or noisy cooling fans"],
 photo=("img8-photo.webp",600,800,"Power module and busbar connections inside an industrial cabinet","Power electronics inside a cabinet"),
 strip=[("work-cabinet-vfd.webp",1000,750,"Motor drive and control cabinet being repaired and commissioned","Drive repair and control panel commissioning"),("work-cabinet-panel.webp",1000,750,"Wiring inside an industrial control panel","Control panel wiring")],
 faq=[("Can you repair drives that other companies gave up on?","We diagnose first and tell you honestly whether repair is practical. Component-level repair often brings drives back that would otherwise be scrapped."),("Do you supply drive spare parts?","Yes. We supply IGBT modules, thyristors, capacitors and cooling fans for your repair stock."),("Do you set up the drive after repair?","Yes. Commissioning and testing are part of the job.")],
 related=["industrial-automation-uganda.html","power-electronics-repair-uganda.html","maintenance-contracts-uganda.html"])
S2["power-electronics-repair-uganda.html"] = dict(
 nav="Power Electronics Repair", icon="chip", card="Power electronics repair",
 blurb="Component-level repair of UPS, inverters, rectifiers, boost converters, drives and LED drivers.",
 title="Power Electronics Repair in Kampala, Uganda | A5",
 desc="Power electronics repair in Kampala and across Uganda: UPS, inverters, rectifiers, boost converters, drives and LED drivers repaired at component level.",
 h1="Power Electronics Repair in Uganda",
 intro="Power electronics sit inside UPS, inverters, drives, chargers and lighting. We repair them at component level, so a failed board or module does not mean a whole new machine.",
 do_title="What we repair",
 do=["UPS systems and inverters","Rectifiers and boost converters","Variable frequency drives and motor controllers","Solar inverters and regulators","LED drivers","Control and power boards, with IGBT, thyristor and diode replacement"],
 signs_title="When to call us",
 signs=["A UPS, inverter or drive shows a power-stage fault","Fuses blow repeatedly","A board shows burnt parts or swollen capacitors","The manufacturer no longer supports the equipment","You want a repair quote before buying a replacement"],
 photo=("work-ups-board.webp",1000,750,"Power electronics board with capacitors and connectors","Power electronics board"),
 strip=[("work-board-mcu.webp",1000,750,"Microcontroller on a circuit board","Controller board"),("work-ups-internals.webp",1000,750,"Open UPS cabinet during repair, showing power and control boards","UPS board-level repair")],
 faq=[("What does component-level repair mean?","We trace the fault to the failed part, such as an IGBT, diode, capacitor or driver, and replace it, instead of swapping the whole board or unit."),("Which equipment can you repair?","UPS, inverters, rectifiers, boost converters, drives, solar regulators and LED drivers, among other power electronics."),("Do you sell the components?","Yes. We supply IGBT modules, thyristors, power diodes, capacitors, transistors, diacs and cooling fans.")],
 related=["ups-repair-uganda.html","vfd-motor-controller-repair-uganda.html","embedded-systems-prototyping-uganda.html"])
S2["refrigeration-cooling-systems-uganda.html"] = dict(
 nav="Refrigeration & Cooling Systems", icon="snow", card="Refrigeration and cooling systems",
 blurb="Repair and maintenance of refrigeration, chillers, pumps and cooling towers for factories and buildings.",
 title="Refrigeration & Cooling Systems Repair Uganda | A5",
 desc="Refrigeration, chiller, pump and cooling tower repair and maintenance in Kampala and across Uganda for factories, offices and industry.",
 h1="Refrigeration & Cooling Systems Repair in Uganda",
 intro="Factories and large buildings depend on cooling. We repair and maintain refrigeration and cooling systems, including chillers, pumps and cooling towers.",
 do_title="Cooling services",
 do=["Refrigeration and cooling system repairs and maintenance","Chillers","Factory pumps and cooling towers maintenance","Motors, drives and controls that run the plant","Preventive maintenance plans","Monitoring of temperatures and equipment status"],
 signs_title="Signs your cooling system needs attention",
 signs=["Temperatures drift above the set point","Unusual noise or vibration from pumps or fans","Frequent trips or shutdowns","Rising energy use for the same cooling","Leaks or scale build-up in the water circuit"],
 photo=IL("illus-cooling.svg",800,600,"Illustration of a chiller connected to a cooling tower with pipes","a chiller connected to a cooling tower"),
 faq=[("Do you maintain chillers and cooling towers?","Yes. We do repair and maintenance of chillers, pumps and cooling towers."),("Can cooling equipment be monitored remotely?","Yes. Our IoT monitoring can track temperatures and equipment status and alert you to problems."),("Do you handle air conditioning too?","Yes. See our air conditioning page for split, cassette, VRF/VRV and packaged units.")],
 related=["air-conditioning-services-uganda.html","air-compressor-services-uganda.html","Monitoring.html"])
S2["maintenance-contracts-uganda.html"] = dict(
 nav="Maintenance Contracts", icon="shield", card="Maintenance contracts",
 blurb="Planned maintenance for UPS, generators, compressors, air conditioning, solar and industrial utility equipment.",
 title="Equipment Maintenance Contracts Kampala, Uganda | A5",
 desc="Maintenance contracting in Kampala and across Uganda for UPS, generators, compressors, air conditioning, solar and industrial equipment. A5 Systems.",
 h1="Equipment Maintenance Contracts in Uganda",
 intro="Planned maintenance costs less than emergency repair. We offer maintenance contracting for industrial and utility equipment, so problems are found and fixed before they stop your operation.",
 do_title="What a maintenance contract can cover",
 do=["UPS systems and battery banks","Generators, including standby sets","Air compressors","Air conditioning and cooling systems","Solar and hybrid power systems","Industrial utility equipment, with spares and technical support"],
 signs_title="Why choose planned maintenance",
 signs=["You want fewer surprise breakdowns","Critical equipment must be ready when needed","You want a record of service visits and equipment condition","You would rather budget than face emergency call-outs"],
 photo=("work-gen-technician.webp",1000,750,"Technician carrying out maintenance on a generator","Generator maintenance"),
 strip=[("work-ups-battery-test.webp",1000,750,"Technician testing UPS battery terminals","Testing UPS battery banks"),("work-gen-laptop.webp",1000,750,"Engineer diagnosing a generator controller fault with a laptop","Generator fault diagnosis and repair")],
 faq=[("How do I get a maintenance contract quote?","Tell us what equipment you have, where it is and how it is used. Call, WhatsApp or email and we will scope a plan."),("Can monitoring be added to a contract?","Yes. Remote monitoring lets us and you see equipment condition between visits."),("Do you also fix breakdowns?","Yes. We provide fault diagnosis and repair as well as planned maintenance.")],
 related=["generator-maintenance-uganda.html","ups-repair-uganda.html","Monitoring.html"])
S2["electrical-installation-wiring-uganda.html"] = dict(
 nav="Industrial Electrical Installation", icon="zap", card="Industrial electrical installation and wiring",
 blurb="Industrial wiring, control panel wiring and connection of generators, UPS, motors and solar systems.",
 title="Industrial Electrical Installation & Wiring Uganda | A5",
 desc="Industrial electrical installation and wiring in Kampala and across Uganda: control panels, motors, generators, UPS and solar systems installed.",
 h1="Industrial Electrical Installation & Wiring in Uganda",
 intro="Reliable equipment starts with correct installation. We provide general industrial wiring and electrical installation, and we commission what we install.",
 do_title="Installation services",
 do=["General industrial wiring","Control panel wiring and modification","Connection of motors and industrial equipment","Installation of UPS, generators and solar systems","Sensors and instrumentation wiring","Testing and commissioning"],
 signs_title="Talk to us when",
 signs=["You are installing new equipment and need it wired and commissioned","A control panel needs repair, upgrade or modification","Wiring is old, untidy or unreliable","You are adding monitoring or automation to existing plant"],
 photo=("work-cabinet-panel.webp",1000,750,"Wiring inside an industrial control panel","Control panel wiring"),
 strip=[("work-cabinet-contactors.webp",1000,750,"Contactors and circuit protection in a control panel","Contactors and protection devices"),("work-transformer.webp",1000,750,"Power transformer at a site","Power transformer at a site")],
 faq=[("Do you install and commission equipment?","Yes. New equipment is installed, tested under real conditions and handed over working."),("Can you modify an existing control panel?","Yes. We repair, upgrade and modify control panels."),("Do you work on generators, UPS and solar installations?","Yes. We install and connect them as well as repairing and maintaining them.")],
 related=["industrial-automation-uganda.html","generator-maintenance-uganda.html","solar-installation-uganda.html"])
ALL = {**S, **S2}

# IoT monitoring cards on Monitoring.html: (heading, icon, "what it does", "what you get", highlighted card?)
MON = [("Equipment and asset monitoring","signal","See how your machines are doing at any time, and get an alert before something fails.","Less downtime and clear facts to base your decisions on.",True),
("Automation and control","cog","Let your equipment and facilities run on their own, from a factory line to a water pump.","Higher output, fewer manual mistakes and lower energy use.",False),
("Power and energy","zap","Keep UPS, solar and generators working well together so your power stays on.","Steady power, longer equipment life and fewer outages.",False),
("Building automation","building","Control air conditioning, security and energy use from one place.","More comfort, lower bills and one simple point of control.",False),
("Lighting control","bulb","Switch and schedule lights automatically, indoors and outdoors.","Lower electricity costs and safer sites.",False),
("Remote solar monitoring","sun","Check how your solar system is performing from your phone or computer.","Instant fault alerts and a clear view of the energy you produce.",False),
("Farm monitoring","leaf","Keep an eye on watering, soil and livestock without being on site.","Less water wasted, better yields and easy farm checks from anywhere.",False),
("Site and environment monitoring","shield","Watch your premises and their conditions day and night.","Know early when something is wrong, and check in from anywhere.",False)]

# ------------------------------------------------------------------ shared pieces
def head(title, desc, path, extra="", noindex=False, ads=True, preload=""):
    canon = SITE + "/" + (path if path != "index.html" else "")
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    e = html.escape
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<!-- Marks the page "js" when JavaScript is available (the phone menu needs it; without JS the menu stays open) -->
<script>document.documentElement.className='js';</script>
{BING}
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- ===== SEO: what Google shows in search results ===== -->
<!-- Page title: keep under ~60 characters, put the main keyword and place first -->
<title>{e(title)}</title>
<!-- Description: the text under the title in results, ~155 characters -->
<meta name="description" content="{e(desc)}">
<meta name="author" content="A5 Systems Uganda">
<!-- Robots: "index, follow" lets search engines list the page; "noindex" hides it -->
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0a1f44">
<!-- Canonical: the ONE official address of this page (stops duplicate-page problems) -->
<link rel="canonical" href="{canon}">
<!-- Language/region: English for Uganda -->
<link rel="alternate" hreflang="en-ug" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">

<!-- ===== Social sharing: preview card when the link is shared on WhatsApp, Facebook, LinkedIn ===== -->
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/A5-systemlogo-Photoroom.png">
<meta property="og:image:width" content="570">
<meta property="og:image:height" content="438">
<meta property="og:image:alt" content="A5 Systems Uganda logo">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_UG">
<meta property="og:site_name" content="A5 Systems Uganda">
<meta name="twitter:card" content="summary">

<!-- Icons: browser tab (favicon) and phone home screen -->
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">

<!-- Main stylesheet: ALL pages share styles.css (colours, layout, buttons, cards) -->
{preload}<link rel="stylesheet" href="styles.css">
{extra}{ADSENSE if ads else ""}
</head>
'''

def header(active):
    """Top of every page: skip link, logo, phone-menu button and main menu. `active` = file to highlight."""
    lis = ""
    for n,h in NAV:
        cur = ' aria-current="page"' if h == active else ""
        lis += f'      <li><a href="{h}"{cur}>{n}</a></li>\n'
    lis += '      <li class="nav-cta"><a href="contact.html">Get a Quote</a></li>\n'
    return f'''<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="A5 Systems Uganda home"><img src="A5-systemlogo.webp" alt="A5 Systems Uganda" width="343" height="227" fetchpriority="high"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span></span></button>
    <nav class="site-nav" id="site-nav" aria-label="Main navigation">
      <ul>
{lis}      </ul>
    </nav>
  </div>
</header>
'''

def cta_band(title="Need an engineer? Talk to A5 Systems Uganda", text=None):
    text = text or f'Call or WhatsApp us, or send us a message. Inquiries: <a href="mailto:{EMAIL}">{EMAIL}</a>'
    return f'''<section class="cta-band">
  <div class="wrap">
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="btn-row">
      <a class="btn" href="tel:{PHONE}">{ic("phone")} Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline" href="contact.html">Give us feedback</a>
    </div>
  </div>
</section>
'''

def footer():
    """Bottom of every page: footer columns, floating WhatsApp button and the phone-menu script."""
    svc = "\n".join(f'      <li><a href="{k}">{v["nav"]}</a></li>' for k,v in S.items()) + f'\n      <li><a href="services.html#specialist">More services</a></li>'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="A5-systemlogo.webp" alt="A5 Systems Uganda" width="343" height="227" loading="lazy">
        <p>Engineering services, systems integration and monitoring for industry, businesses, homes and farms across Uganda.</p>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h3>Company</h3>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About us</a></li>
          <li><a href="service-areas-uganda.html">Areas we serve</a></li>
          <li><a href="services.html">All services</a></li>
          <li><a href="products.html">Products</a></li>
          <li><a href="Monitoring.html">IoT Monitoring</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="privacy.html">Privacy policy</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li>Phone / WhatsApp:<br><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></li>
          <li>Email:<br><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 A5 Systems Uganda. All rights reserved.</span>
      <span>Serving Kampala, Wakiso and all of Uganda</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{PHONE.lstrip('+')}" aria-label="Chat with us on WhatsApp">{ic("phone")}<span>WhatsApp</span></a>
<!-- PHONE MENU SCRIPT: the hamburger button opens/closes the main menu on small screens -->
<script>
(function () {{
  var b = document.querySelector('.nav-toggle'), n = document.getElementById('site-nav');
  if (!b || !n) return;                           // nothing to do if the menu is missing
  b.addEventListener('click', function () {{
    var open = n.classList.toggle('open');        // show/hide the menu (see .site-nav.open in styles.css)
    b.setAttribute('aria-expanded', open ? 'true' : 'false');   // tells screen readers the state
  }});
}})();
</script>
</body>
</html>
'''

def ld(obj):
    """Wrap a Python dict as JSON-LD structured data (helps Google show rich results)."""
    return ('<!-- STRUCTURED DATA (JSON-LD): tells Google about the business, services, FAQs and breadcrumbs.\n'
            '     Keep it in step with the visible text on the page. -->\n'
            '<script type="application/ld+json">\n' + json.dumps(obj, indent=2) + '\n</script>\n')


def gal(items):
    """Photo gallery. items = list of (file, width, height, alt, caption). Empty caption = graphic only."""
    out='<div class="gallery">\n'
    for f,w,h,alt,cap in items:
        cap_html = f'<figcaption>{cap}</figcaption>' if cap else ''
        out+=f'      <figure><img src="images/{f}" width="{w}" height="{h}" loading="lazy" alt="{alt}">{cap_html}</figure>\n'
    return out+'    </div>'

def crumbs(items):
    """Breadcrumb structured data for Google. items = [(name, file), ...]"""
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+"/"+p if p else SITE+"/"} for i,(n,p) in enumerate(items)]}

def page_hero(h1, lead, trail):
    """Dark banner at the top of inner pages: breadcrumb, h1 heading and intro line. Opens <main>."""
    bc = ' &rsaquo; '.join(f'<a href="{p}">{n}</a>' for n,p in trail[:-1]) + (' &rsaquo; ' if len(trail)>1 else '') + trail[-1][0]
    return f'''<main id="main">
<section class="page-hero">
  <div class="wrap">
    <p class="breadcrumb">{bc}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''

BUSINESS = {
 "@type":"ProfessionalService","@id":SITE+"/#business","name":"A5 Systems Uganda","url":SITE+"/",
 "logo":SITE+"/A5-systemlogo-Photoroom.png","image":SITE+"/A5-systemlogo-Photoroom.png",
 "telephone":PHONE,"email":EMAIL,
 "description":"Engineering services in Uganda: UPS and power electronics repair, generator maintenance, solar systems, building management systems, industrial automation and IoT monitoring.",
 "address":{"@type":"PostalAddress","streetAddress":"Kitende A, Kajjansi T/C","addressLocality":"Kajjansi","addressRegion":"Wakiso","addressCountry":"UG"},
 "areaServed":[{"@type":"Country","name":"Uganda"},{"@type":"City","name":"Kampala"},{"@type":"AdministrativeArea","name":"Wakiso"},{"@type":"City","name":"Entebbe"},{"@type":"City","name":"Mukono"}],
 "knowsAbout":["UPS repair","Generator maintenance","Solar installation","Building management systems","Industrial automation","IoT monitoring","Power electronics repair","VFD repair","Air conditioning","Air compressors","Energy storage","Refrigeration and cooling","Maintenance contracts"],
 "contactPoint":{"@type":"ContactPoint","telephone":PHONE,"email":EMAIL,"contactType":"customer service","areaServed":"UG","availableLanguage":"English"},
 "hasOfferCatalog":{"@type":"OfferCatalog","name":"Engineering services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":v["nav"],"url":SITE+"/"+k}} for k,v in ALL.items()]},
}

import re

# Short explanations inserted as HTML comments in front of these page parts.
TAG_NOTES = [
    (r'<a class="skip-link"',            'ACCESSIBILITY: "skip to main content" link, only visible when a keyboard user presses Tab'),
    (r'<header class="site-header">',    'SITE HEADER: logo + main menu. Menu links come from NAV in tools/build_site.py (or edit the links below)'),
    (r'<button class="nav-toggle"',      'PHONE MENU BUTTON: hidden on desktop, opens the menu on phones (script at the bottom of the page)'),
    (r'<nav class="site-nav"',           'MAIN MENU: one <li> per page; the last one is the highlighted "Get a Quote" button'),
    (r'<main id="main">',                'MAIN PAGE CONTENT starts here'),
    (r'<div class="cards',               'CARD GRID: every <article class="card"> is one card'),
    (r'<ol class="steps">',              'PROCESS STEPS: every <li> is one numbered step'),
    (r'<div class="faq">',               'FAQ ACCORDION: every <details> is one question (click to open). Also listed in the JSON-LD data in <head>'),
    (r'<div class="gallery">',           'PHOTO GALLERY: every <figure> is one photo (files are in images/)'),
    (r'<figure><img src="images/illus-', 'GRAPHIC ONLY: vector illustration with no caption. To change it, edit or replace the .svg file in images/'),
    (r'<figure class="flow">',           'GRAPHIC ONLY: IoT flow diagram, no caption. Edit images/illus-iot-flow.svg to change it'),
    (r'<form class="form"',              'CONTACT FORM: delivered by EmailJS (see the script at the bottom of this page)'),
    (r'<footer class="site-footer">',    'SITE FOOTER: same on every page (links, contact details, copyright)'),
    (r'<a class="wa-float"',             'FLOATING WHATSAPP BUTTON: bottom-right corner on every page'),
]

def annotate(page):
    """Insert readable HTML comments so each part of a generated page is easy to find later."""
    # 1) a comment before every <section>, named after its first heading
    def section_note(m):
        after = m.string[m.end():m.end()+2500]
        h = re.search(r'<h[12][^>]*>(.*?)</h[12]>', after, re.S)
        name = re.sub(r'<[^>]+>', '', h.group(1)).strip() if h else 'content'
        name = name.replace('--', '-')
        return '<!-- ===== SECTION: ' + name + ' ===== -->\n' + m.group(0)
    page = re.sub(r'<section[^>]*>', section_note, page)
    # 2) a comment before other well-known parts
    for pattern, note in TAG_NOTES:
        page = re.sub('(' + pattern + ')', '<!-- ' + note + ' -->\n\\1', page, count=0)
    return page

def write(name, content):
    """Save one generated page to the website folder (after adding readable HTML comments)."""
    if name.endswith('.html'):
        content = annotate(content)
    with open(os.path.join(ROOT,name),"w",encoding="utf-8",newline="\n") as f: f.write(content)
    print("wrote", name)

def service_cards(keys=None, link_text="Learn more", src=None):
    """Return the HTML for the grid of service cards. src=None -> core services + monitoring card."""
    out = ""
    for k,v in (src or S).items():
        out += f'''    <article class="card">
      <span class="card-icon">{ic(v["icon"])}</span>
      <h3><a href="{k}">{v["card"]}</a></h3>
      <p>{v["blurb"]}</p>
      <span class="card-link">{link_text} {ic("arrow")}</span>
    </article>
'''
    if src is not None: return out
    out += f'''    <article class="card">
      <span class="card-icon">{ic("signal")}</span>
      <h3><a href="Monitoring.html">Monitoring and IoT services</a></h3>
      <p>Real-time visibility, predictive maintenance and data-driven insight for equipment, power, solar, buildings and farms.</p>
      <span class="card-link">{link_text} {ic("arrow")}</span>
    </article>
'''
    return out

def steps_html(dark=False):
    """Return the numbered "how we work" steps."""
    return '<ol class="steps">\n' + "\n".join(f'  <li><h3>{t}</h3><p>{d}</p></li>' for t,d in STEPS) + '\n</ol>\n'

# ================================================================== HOME
TAGLINE = "Engineering Services | Systems integration | Industrial Electrical and Mechanical Engineering | Generators and UPS"
P1 = "We diagnose complex faults, upgrade legacy systems, and install and commission new equipment. We provide unmatched technical support."
P2 = "Our portfolio spans a broad range of industrial equipment, UPS, Generators, compressors, and chillers, Remote monitoring solutions, Hybrid inverters, solar systems, Building management systems, and energy optimization"


HOME_FAQ=[("What engineering services does A5 Systems Uganda offer?","We provide UPS and power electronics repair, generator maintenance, solar and hybrid systems, energy storage, air conditioning, air compressor services, building management systems, industrial automation, lighting, embedded systems and IoT monitoring."),
("Where do you work?","We are based in Kitende, Kajjansi, Wakiso District, and serve customers in Kampala, Wakiso and across Uganda."),
("Can you repair a UPS or generator?","Yes. We install, repair and maintain UPS systems and inverters of all brands, and we service and repair generators of all sizes. Tell us the make, model and fault, and we will advise on the next step."),
("Do you offer maintenance contracts?","Yes. We offer maintenance contracting for UPS, generators, compressors, air conditioning, solar and industrial utility equipment."),
("Do you supply spare parts?","Yes. We supply IGBT modules, thyristors, power diodes, capacitors, cooling fans and generator spares."),
("How do I get a quote?","Call or WhatsApp +256 757 732 991, email sales@afive.cc, or use our contact form. A photo of the equipment or its nameplate helps us respond faster.")]
HOME_FAQ_HTML='<section class="section section-alt">\n  <div class="wrap">\n    <div class="section-head"><span class="kicker">Questions</span><h2>Engineering services in Uganda: common questions</h2></div>\n    <div class="faq">\n' + "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q,a in HOME_FAQ) + '\n    </div>\n  </div>\n</section>\n'
HOME_PILLS='<ul class="pills" style="justify-content:center;margin-top:28px">' + "".join(f'<li><a href="{k}">{v["nav"]}</a></li>' for k,v in S2.items()) + '<li><a href="service-areas-uganda.html">Areas we serve</a></li></ul>'

home = head("A5 Systems Uganda | Engineering, UPS, Generators & BMS",
  "Engineering services in Kampala and across Uganda: UPS and power electronics repair, generators, solar, building management systems and IoT monitoring.",
  "index.html",
  extra=ld({"@context":"https://schema.org","@graph":[BUSINESS,{"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"A5 Systems Uganda","publisher":{"@id":SITE+"/#business"},"inLanguage":"en"},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in HOME_FAQ]}]}),
  preload='<link rel="preload" as="image" href="images/hero-1600.webp" imagesrcset="images/hero-800.webp 800w, images/hero-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">\n')
home += header("index.html") + f'''<main id="main">
<section class="hero" id="home">
  <div class="hero-bg"><img src="images/hero-1600.webp" srcset="images/hero-800.webp 800w, images/hero-1600.webp 1600w" sizes="100vw" alt="" width="1600" height="1200" fetchpriority="high"></div>
  <div class="wrap">
    <span class="eyebrow">A5 Systems Uganda</span>
    <h1>{TAGLINE}</h1>
    <p class="lead">{P1}</p>
    <p class="lead">{P2}</p>
    <div class="btn-row">
      <a class="btn" href="services.html">Discover our services {ic("arrow")}</a>
      <a class="btn btn-outline" href="contact.html">Get a quote</a>
    </div>
  </div>
</section>

<section class="trust" aria-label="Why choose A5 Systems">
  <div class="wrap">
    <ul>
      <li>{ic("pin")} Serving Kampala, Wakiso and all Uganda</li>
      <li>{ic("zap")} All brands of UPS and inverters</li>
      <li>{ic("cog")} Generators of all sizes</li>
      <li>{ic("phone")} <a href="tel:{PHONE}">Call {PHONE_DISPLAY}</a></li>
    </ul>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">What we do</span>
      <h2>Engineering services for power, equipment and buildings</h2>
      <p>From UPS and generators to solar, air conditioning and building management, one team takes care of the technical work.</p>
    </div>
    <div class="cards">
{service_cards()}    </div>
    {HOME_PILLS}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">How we work</span>
      <h2>From fault to fixed</h2>
      <p>A simple process, whether it is a single failed UPS or a whole new installation.</p>
    </div>
{steps_html()}  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Who we help</span>
      <h2>Technical support for every kind of customer</h2>
    </div>
    <div class="cards four">
      <article class="card card-plain"><span class="card-icon">{ic("factory")}</span><h3>Industry</h3><p>UPS, generators, compressors, chillers, drives and controls kept running, with fault diagnosis and maintenance contracts.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("building")}</span><h3>Businesses and buildings</h3><p>Power backup, air conditioning, lighting and building management systems that keep premises comfortable and efficient.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("home")}</span><h3>Homes</h3><p>Solar systems, hybrid inverters, battery backup and lighting for reliable power at home.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("leaf")}</span><h3>Farms</h3><p>Solar power and remote monitoring for watering, soil and livestock, so you can check the farm from anywhere.</p></article>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Our work in pictures</span>
      <h2>Real equipment, real repairs, real sites</h2>
    </div>
    ''' + gal([P("gen-service","Technician carrying out scheduled maintenance on a standby generator","Generator maintenance and servicing"),P("gen-laptop","Engineer diagnosing a generator controller fault with a laptop","Generator fault diagnosis and repair"),P("ups-room","Installed UPS cabinets and battery banks in an equipment room","UPS installation and commissioning"),P("ups-battery-test","Technician testing UPS battery terminals during maintenance","UPS battery testing and replacement"),P("team-site","A5 Systems engineers inspecting an electrical cabinet during a site visit","On-site inspection and maintenance"),P("ups-internals","Open UPS cabinet during repair, showing power and control boards","UPS board-level repair"),P("ac-service","Technician servicing a wall-mounted air conditioner","Air conditioner servicing and repair"),P("cabinet-vfd","Motor drive and control cabinet being repaired and commissioned","Drive repair and control panel commissioning")]) + f'''
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:0">
      <span class="kicker">IoT monitoring</span>
      <h2>Know about problems before they stop your operation</h2>
      <p>We give asset owners and managers complete visibility and control over their equipment, with real-time monitoring, predictive maintenance and alerts on your phone.</p>
      <div class="btn-row" style="justify-content:center"><a class="btn" href="Monitoring.html">Explore IoT monitoring {ic("arrow")}</a></div>
    </div>
  </div>
</section>

{HOME_FAQ_HTML}<section class="section">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:24px"><h2>Explore more</h2></div>
    <ul class="pills" style="justify-content:center">
      <li><a href="services.html">Core services</a></li>
      <li><a href="products.html">Our Solutions</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="contact.html">Give us feedback</a></li>
    </ul>
  </div>
</section>
</main>
''' + cta_band() + footer()
write("index.html", home)

# ================================================================== SERVICES
svcs = head("Engineering & Repair Services in Uganda | A5 Systems",
  "UPS repair, generator maintenance, solar installation, air conditioning, energy storage, lighting, embedded systems and IoT monitoring in Uganda.",
  "services.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("Services","services.html")]),{"@type":"ItemList","name":"A5 Systems Uganda services","itemListElement":[{"@type":"ListItem","position":n+1,"name":v["nav"],"url":SITE+"/"+k} for n,(k,v) in enumerate(ALL.items())]}]}))
svcs += header("services.html") + page_hero("Engineering Services in Uganda",
  "We diagnose complex faults, upgrade legacy systems, and install and commission new equipment. Choose a service to see what we do and how we can help.",
  [("Home","index.html"),("Services","")]) + f'''<section class="section">
  <div class="wrap">
    <div class="cards">
{service_cards(link_text="View service")}    </div>
  </div>
</section>
<section class="section section-alt" id="specialist">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Specialist services</span><h2>More ways we can help</h2></div>
    <div class="cards">
{service_cards(link_text="View service", src=S2)}    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">How we work</span><h2>One process, every service</h2></div>
{steps_html()}  </div>
</section>
</main>
''' + cta_band("Not sure which service you need?", f'Describe the problem and we will point you in the right direction. Call, WhatsApp or email <a href="mailto:{EMAIL}">{EMAIL}</a>.') + footer()
write("services.html", svcs)

# ================================================================== LANDING PAGES
for fn,v in ALL.items():
    photo_html = ""
    if v.get("photo"):
        f,w,h,alt,cap = v["photo"]
        cap_html = f'<figcaption>{cap}</figcaption>' if cap else ''   # illustrations have no caption
        photo_html = f'<figure><img src="images/{f}" width="{w}" height="{h}" loading="lazy" alt="{alt}">{cap_html}</figure>'
    do_list = '<ul class="checks">\n' + "\n".join(f"      <li>{i}</li>" for i in v["do"]) + '\n    </ul>'
    do_block = f'''<div>
    <h2>{v["do_title"]}</h2>
    {do_list}
    {v.get("extra","")}
    <div class="btn-row"><a class="btn" href="contact.html">Request a quote</a><a class="btn btn-ghost" href="tel:{PHONE}">{ic("phone")} Call now</a></div>
  </div>'''
    if photo_html:
        first = f'<section class="section"><div class="wrap split">{do_block}{photo_html}</div></section>'
    else:
        first = f'<section class="section"><div class="wrap" style="max-width:860px">{do_block}</div></section>'
    signs = '<ul class="checks warn">\n' + "\n".join(f"      <li>{i}</li>" for i in v["signs"]) + '\n    </ul>'
    faqs = "\n".join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q,a in v["faq"])
    rel = "\n".join(f'      <li><a href="{r}">{(ALL[r]["nav"] if r in ALL else "IoT Monitoring")}</a></li>' for r in v["related"])
    strip = ""
    if v.get("strip"):
        strip = '<section class="section" style="padding-top:0"><div class="wrap"><h2 style="font-size:1.4rem">From the field</h2>' + gal(v["strip"]) + '</div></section>'
    body = page_hero(v["h1"], v["intro"], [("Home","index.html"),("Services","services.html"),(v["nav"],"")]) + first + strip + f'''
<section class="section section-alt">
  <div class="wrap" style="max-width:860px">
    <h2>{v["signs_title"]}</h2>
    {signs}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">How we work</span><h2>What to expect when you call us</h2></div>
{steps_html()}  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Frequently asked questions</h2></div>
    <div class="faq">
{faqs}
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap" style="max-width:860px">
    <h2 style="font-size:1.4rem">{html.escape(v["nav"])} in Kampala, Wakiso and across Uganda</h2>
    <p>A5 Systems Uganda is based in Kitende, Kajjansi, Wakiso District. We support customers in Kampala, Wakiso, Entebbe, Mukono and across Uganda. See the <a href="service-areas-uganda.html">areas we serve</a> or <a href="contact.html">request a quote</a>.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 style="font-size:1.3rem">Related services</h2>
    <ul class="pills">
{rel}
      <li><a href="services.html">All services</a></li>
    </ul>
  </div>
</section>
</main>
'''
    schema = ld({"@context":"https://schema.org","@graph":[
      {"@type":"Service","name":v["h1"],"serviceType":v["nav"],"provider":{"@id":SITE+"/#business"},"areaServed":{"@type":"Country","name":"Uganda"},"url":SITE+"/"+fn,"description":v["desc"]},
      crumbs([("Home",""),("Services","services.html"),(v["nav"],fn)]),
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in v["faq"]]}]})
    write(fn, head(v["title"], v["desc"], fn, extra=schema) + header("services.html") + body + cta_band() + footer())

# ================================================================== MONITORING (keep filename: existing indexed URL)
mon_cards = ""
for n,i,w,g,f in MON:
    mon_cards += f'''    <article class="card card-plain{' featured' if f else ''}">
      <span class="card-icon">{ic(i)}</span>
      <h3>{n}</h3>
      <dl><dt>What it does</dt><dd>{w}</dd><dt>What you get</dt><dd>{g}</dd></dl>
    </article>
'''
mon_faq = [("Do I need to replace my equipment to monitor it?","Often not. Sensors and gateways can usually be added to existing equipment, so you keep what you have and gain visibility of it."),
           ("Can I see the information on my phone?","Yes. You can check your equipment from your phone or computer and receive alerts when something needs attention."),
           ("What kinds of equipment can be monitored?","Generators, UPS, solar systems, air compressors, buildings and lighting, farms and general site conditions. Tell us what matters to you and we will advise.")]
mon = head("IoT Monitoring & Asset Management Systems Uganda | A5",
  "IoT asset management and remote monitoring in Uganda: generators, UPS, solar, buildings, lighting and agriculture. Real-time data, alerts and dashboards.",
  "Monitoring.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("IoT Monitoring","Monitoring.html")]),{"@type":"Service","name":"IoT monitoring and asset management","provider":{"@id":SITE+"/#business"},"areaServed":{"@type":"Country","name":"Uganda"},"url":SITE+"/Monitoring.html"},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in mon_faq]}]}))
mon += header("Monitoring.html") + page_hero("IoT Monitoring &amp; Asset Management Solutions",
  "We help you see what your equipment, power and buildings are doing, all the time, from anywhere. You get alerts when something needs attention, so you can fix small problems before they become expensive ones.",
  [("Home","index.html"),("IoT Monitoring","")]) + f'''<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">What we can monitor and control</span><h2>Monitoring that fits how you work</h2></div>
    <div class="cards">
{mon_cards}    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">How it works</span><h2>Three simple parts</h2></div>
    <figure class="flow"><img src="images/illus-iot-flow.svg" width="1000" height="300" loading="lazy" alt="Diagram: equipment with sensors sends data through a gateway to the cloud, shown on your phone or computer"></figure>
    <ol class="steps">
      <li><h3>Sensors and meters</h3><p>Small devices are fitted to your equipment to measure what matters: power, temperature, runtime, levels and more.</p></li>
      <li><h3>Secure connection</h3><p>A gateway sends the readings to the cloud so they are stored and analysed.</p></li>
      <li><h3>Dashboards and alerts</h3><p>You see live status on your phone or computer and get an alert when something is wrong.</p></li>
    </ol>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Monitoring starts at the equipment</span><h2>The data is already there</h2><p>Generators, UPS and inverters already measure load, pressure and temperature. We connect that information to dashboards and alerts.</p></div>
    ''' + gal([P("gen-controller","Generator controller showing generation load","Generator controller showing load"),P("gen-controller2","Generator controller showing engine oil pressure","Generator controller showing engine oil pressure")]) + f'''
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Frequently asked questions</h2></div>
    <div class="faq">
''' + "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q,a in mon_faq) + '''
    </div>
  </div>
</section>
</main>
''' + cta_band("Want to see your equipment on a dashboard?", f'Ask for a demo. Call, WhatsApp or email <a href="mailto:{EMAIL}">{EMAIL}</a>.') + footer()
write("Monitoring.html", mon)

# ================================================================== PRODUCTS
def pcard(icon,t,items,note=""):
    """One product card on products.html."""
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'''    <article class="card card-plain">
      <span class="card-icon">{ic(icon)}</span>
      <h3>{t}</h3>
      {"<p>"+note+"</p>" if note else ""}
      <ul class="checks">{li}</ul>
    </article>
'''
prod = head("Power Electronics, Controllers & Monitoring Products | A5",
  "Supply of IGBT modules, thyristors, diodes, capacitors, custom controllers, PLCs, asset management systems and smart plugs in Uganda.",
  "products.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("Products","products.html")])]}))
prod += header("products.html") + page_hero("Products &amp; Supplies",
  "Power electronics components for your repair stock, controllers and monitoring systems built for your application, and everyday electrical accessories.",
  [("Home","index.html"),("Products","")]) + f'''<section class="section">
  <div class="wrap">
    <div class="cards">
{pcard("chip","Custom controllers",["PLCs","Application-tailored controllers","Versatile controllers for industrial and consumer applications"])}{pcard("signal","Asset management system",["Support software","Visual customization to your branding","Data acquisition modules and gateways","Control modules","Cloud services"],'See <a href="Monitoring.html">IoT monitoring</a> for how it works.')}{pcard("zap","Power electronics",["IGBT modules for industrial UPS, drives and solar inverters","Thyristors","Transistors and diacs","Electrolytic capacitors and cooling fans","Technical support"])}{pcard("wrench","Power diodes",["Fast recovery diodes","Ultra-fast diodes"],"For your repair stock.")}{pcard("building","Energy management systems",["Supporting software and hardware","Integration services"],'See <a href="building-management-systems-uganda.html">building management systems</a>.')}{pcard("home","Electrical accessories",["Durable, heavy-duty extension cables for industrial and domestic use","Wi-Fi smart plug sockets to control appliances remotely"])}    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Components for real repairs</span><h2>Parts we work with every day</h2></div>
    ''' + gal([P("ups-board","Power electronics board with capacitors and connectors","Power electronics board"),P("board-mcu","Microcontroller on a circuit board","Controller board"),P("ups-internals","Open UPS cabinet during repair, showing power and control boards","UPS board-level repair")]) + f'''
  </div>
</section>
<section class="section">
  <div class="wrap" style="max-width:860px">
    <h2>How to order or ask about a part</h2>
    <ul class="checks">
      <li>Send the part number or a clear photo of the part or nameplate</li>
      <li>Tell us the equipment it is for (for example the UPS or drive model)</li>
      <li>Call, WhatsApp or email us and we will confirm availability and a quote</li>
    </ul>
    <div class="btn-row"><a class="btn btn-wa" href="https://wa.me/{PHONE.lstrip('+')}">WhatsApp us</a><a class="btn btn-ghost" href="contact.html">Send a message</a></div>
  </div>
</section>
</main>
''' + cta_band("Looking for a component or a custom solution?") + footer()
write("products.html", prod)

# ================================================================== ABOUT
ab = head("About A5 Systems Uganda | Engineering Company in Wakiso",
  "A5 Systems Uganda integrates technology and reliability for power, automation, energy management and infrastructure. Based in Kitende, Kajjansi, Wakiso.",
  "about.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("About","about.html")]),{"@type":"AboutPage","url":SITE+"/about.html","about":{"@id":SITE+"/#business"}}]}))
ab += header("about.html") + page_hero("About A5 Systems Uganda",
  "We specialize in integrating technology with reliability to solve real-world challenges, whether it is powering critical operations, energy management, automating processes or upgrading infrastructure.",
  [("Home","index.html"),("About","")]) + f'''<section class="section">
  <div class="wrap split">
    <div>
      <h2>Who we are</h2>
      <p>With a commitment to quality, innovation and customer satisfaction, we build a more efficient and future-ready environment.</p>
      <p>We deliver a wide portfolio of technical services for power electronics, automation, instrumentation and industrial equipment.</p>
      <p>We support industries with tailored technical support services, from troubleshooting and repairing complex systems to maintaining and installing advanced technologies.</p>
      <p>Registered and located in Uganda: {ADDRESS}.</p>
      <div class="btn-row"><a class="btn" href="contact.html">Contact us today</a><a class="btn btn-ghost" href="services.html">Our services</a></div>
    </div>
    <figure><img src="images/work-team-site.webp" width="1000" height="750" loading="lazy" alt="A5 Systems team inspecting an electrical cabinet on site"><figcaption>The A5 Systems team on a site visit</figcaption></figure>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">What we stand for</span><h2>Built on four commitments</h2></div>
    <div class="cards four">
      <article class="card card-plain"><span class="card-icon">{ic("shield")}</span><h3>Reliability</h3><p>Technology that keeps critical operations powered and running.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("check")}</span><h3>Quality</h3><p>Faults traced to their cause and fixed properly, with equipment commissioned and tested.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("chip")}</span><h3>Innovation</h3><p>Monitoring, automation and custom electronics that make systems more efficient and future-ready.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("phone")}</span><h3>Customer satisfaction</h3><p>Unmatched technical support before, during and after every job.</p></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Our expertise</span><h2>What we work on</h2></div>
    <div class="cards four">
      <article class="card card-plain"><h3>Power</h3><ul class="checks"><li>UPS and inverters</li><li>Generators</li><li>Solar and hybrid systems</li><li>Battery storage</li></ul></article>
      <article class="card card-plain"><h3>Industrial equipment</h3><ul class="checks"><li>Air compressors</li><li>Chillers, pumps and cooling towers</li><li>Drives and motor controllers</li><li>PLCs and instrumentation</li></ul></article>
      <article class="card card-plain"><h3>Buildings and energy</h3><ul class="checks"><li>Building management systems</li><li>Air conditioning</li><li>Lighting and lighting control</li><li>Energy optimization</li></ul></article>
      <article class="card card-plain"><h3>Electronics and IoT</h3><ul class="checks"><li>Power electronics repair</li><li>Embedded systems and prototyping</li><li>Remote monitoring</li><li>Asset management</li></ul></article>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">On site</span><h2>Hands-on technical work</h2></div>
    ''' + gal([P("gen-laptop","Engineer diagnosing a generator controller fault with a laptop","Generator fault diagnosis and repair"),P("ups-battery-test","Technician testing UPS battery terminals","Testing UPS battery banks"),P("gen-service","Technician servicing a standby generator","Servicing a generator"),P("ac-service","Technician servicing a wall-mounted air conditioner","Air conditioner servicing and repair")]) + f'''
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">How we work</span><h2>A clear process</h2></div>
{steps_html()}  </div>
</section>
</main>
''' + cta_band() + footer()
write("about.html", ab)

# ================================================================== CONTACT
ct = head("Contact A5 Systems Uganda | Request a Quote",
  "Contact A5 Systems Uganda by phone, WhatsApp, email or form for UPS, generator, solar, BMS and engineering services. Kitende, Kajjansi, Wakiso.",
  "contact.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("Contact","contact.html")]),{"@type":"ContactPage","url":SITE+"/contact.html","mainEntity":{"@id":SITE+"/#business"}}]}) + '<script src="https://cdn.emailjs.com/dist/email.min.js" defer></script>\n')
ct += header("contact.html") + page_hero("Contact A5 Systems Uganda",
  "Tell us what you need. Call or WhatsApp for the fastest reply, or send a message and we will get back to you.",
  [("Home","index.html"),("Contact","")]) + f'''<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Get in touch</h2>
      <ul class="contact-list">
        <li><span class="card-icon">{ic("phone")}</span><div><strong>Phone / WhatsApp</strong><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div></li>
        <li><span class="card-icon">{ic("mail")}</span><div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="card-icon">{ic("pin")}</span><div><strong>Location</strong>{ADDRESS}<br>Serving Kampala, Wakiso and all of Uganda</div></li>
      </ul>
      <a class="btn btn-wa" href="https://wa.me/{PHONE.lstrip('+')}">{ic("phone")} Chat on WhatsApp</a>
      <h3 style="margin-top:32px">To help us reply faster, include</h3>
      <ul class="checks">
        <li>What equipment it is (make and model if you know)</li>
        <li>What is happening, and any fault codes or alarms</li>
        <li>Where the equipment is located</li>
        <li>A photo of the equipment or its nameplate, on WhatsApp</li>
      </ul>
    </div>
    <div>
      <form class="form" id="contact-form" method="POST">
        <h2 style="font-size:1.5rem">Send us a message</h2>
        <div class="form-group"><label for="name">Name</label><input type="text" id="name" name="name" autocomplete="name" required></div>
        <div class="form-group"><label for="email">Email</label><input type="email" id="email" name="email" autocomplete="email" required></div>
        <div class="form-group"><label for="message">Message</label><textarea id="message" name="message" rows="6" required></textarea></div>
        <button type="submit" class="btn" id="send-btn">Send message</button>
        <div class="form-status" id="form-status" role="status" aria-live="polite" hidden></div>
        <noscript><p>The form needs JavaScript. Please email <a href="mailto:{EMAIL}">{EMAIL}</a> instead.</p></noscript>
      </form>
    </div>
  </div>
</section>
</main>
<!-- CONTACT FORM SCRIPT: sends the message by email through EmailJS (https://www.emailjs.com).
     The IDs below (public key, service, template) come from the EmailJS dashboard. -->
<script>
window.addEventListener('DOMContentLoaded', function () {{
  // Find the form, the message box under it, and the Send button
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');
  var btn = document.getElementById('send-btn');
  // Show a message under the form: cls 'ok' = green success, 'err' = red error
  function show(cls, msg) {{ status.className = 'form-status ' + cls; status.textContent = msg; status.hidden = false; }}
  // When Send is pressed: stop the normal page reload, then send through EmailJS
  form.addEventListener('submit', function (event) {{
    event.preventDefault();
    if (!window.emailjs) {{ show('err', 'Could not send right now. Please email {EMAIL} or use WhatsApp.'); return; }}
    emailjs.init('nNTicm7T6tckV92re');   // EmailJS public key (safe to be visible)
    btn.disabled = true; btn.textContent = 'Sending...';
    emailjs.sendForm('service_mteco95', 'template_l32up3i', form).then(
      function () {{ show('ok', 'Thank you. Your message has been sent and we will reply soon.'); form.reset(); btn.disabled = false; btn.textContent = 'Send message'; }},
      function () {{ show('err', 'Sorry, the message could not be sent. Please try again, or email {EMAIL}.'); btn.disabled = false; btn.textContent = 'Send message'; }}
    );
  }});
}});
</script>
''' + footer()
write("contact.html", ct)

# ================================================================== PRIVACY
pv = head("Privacy Policy | A5 Systems Uganda",
  "How A5 Systems Uganda handles information from visitors to afive.cc, including the contact form and Google advertising cookies.",
  "privacy.html")
pv += header("") + page_hero("Privacy Policy", "How we handle information on this website.", [("Home","index.html"),("Privacy policy","")]) + f'''<section class="section">
  <div class="wrap prose">
    <p><em>Last updated: 28 September 2026</em></p>
    <h2>Who we are</h2>
    <p>This website (afive.cc) is operated by A5 Systems Uganda, {ADDRESS}. You can contact us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>Information you give us</h2>
    <p>If you use the contact form we receive your name, email address and message, and we use them only to reply to you and provide the service you asked about. The form is delivered through the EmailJS service. If you contact us by phone, WhatsApp or email, we use the details you give us in the same way. We do not sell your information.</p>
    <h2>Advertising and cookies</h2>
    <p>This site may show advertising provided by Google AdSense. Google and its partners may use cookies to serve ads based on your visits to this and other websites. You can manage personalised advertising in your Google Ads Settings and in your browser settings.</p>
    <h2>Links to other sites</h2>
    <p>Our pages may link to other websites, such as WhatsApp. We are not responsible for the content or privacy practices of other sites.</p>
    <h2>Your choices</h2>
    <p>You can ask us to correct or delete the information you have sent us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>Changes</h2>
    <p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>
  </div>
</section>
</main>
''' + footer()
write("privacy.html", pv)


# ================================================================== SERVICE AREAS
areas_links = "".join(f'<li><a href="{k}">{v["nav"]}</a></li>' for k,v in ALL.items()) + '<li><a href="Monitoring.html">IoT Monitoring</a></li>'
afaq=[("Do you work outside Kampala?","Yes. We are based in Wakiso District and support customers in Kampala, Wakiso, Entebbe, Mukono and across Uganda. Tell us where the equipment is and we will discuss how to support the job."),
      ("Which services are available in my area?","All of our services, from UPS and generator work to solar, air conditioning, building management systems and IoT monitoring. Call us to confirm arrangements for your location."),
      ("How do I ask for a visit or a quote?","Call or WhatsApp +256 757 732 991, email sales@afive.cc or use the contact form, and include the location and a photo of the equipment if you can.")]
ar = head("Engineering Services in Kampala, Wakiso & Uganda | A5",
  "UPS, generator, solar, air conditioning, BMS and industrial engineering services in Kampala, Wakiso, Entebbe, Mukono and across Uganda. A5 Systems.",
  "service-areas-uganda.html", extra=ld({"@context":"https://schema.org","@graph":[crumbs([("Home",""),("Areas we serve","service-areas-uganda.html")]),{"@type":"WebPage","url":SITE+"/service-areas-uganda.html","about":{"@id":SITE+"/#business"}},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in afaq]}]}))
ar += header("") + page_hero("Engineering Services in Kampala, Wakiso and Across Uganda",
  "A5 Systems Uganda is based in Kitende, Kajjansi, Wakiso District. We provide engineering, repair, maintenance and installation services to customers throughout Uganda.",
  [("Home","index.html"),("Areas we serve","")]) + f'''<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Where we work</span><h2>Areas we serve</h2></div>
    <div class="cards four">
      <article class="card card-plain"><span class="card-icon">{ic("pin")}</span><h3>Kampala</h3><p>UPS, generator, solar, air conditioning, building systems and industrial engineering support for businesses and homes in Kampala.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("pin")}</span><h3>Wakiso, Kajjansi and Kitende</h3><p>Our base is Kitende, Kajjansi in Wakiso District, so customers across Wakiso are close to our team.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("pin")}</span><h3>Entebbe and Mukono</h3><p>We provide engineering services in Entebbe, Mukono and the surrounding areas. Call us to arrange a visit.</p></article>
      <article class="card card-plain"><span class="card-icon">{ic("pin")}</span><h3>Elsewhere in Uganda</h3><p>Need help in Jinja, Mbarara, Masaka, Gulu, Mbale, Fort Portal or elsewhere? Tell us about the job and we will discuss how to support it.</p></article>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Services</span><h2>Everything we offer, wherever you are</h2></div>
    <ul class="pills" style="justify-content:center">{areas_links}</ul>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Frequently asked questions</h2></div>
    <div class="faq">
''' + "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q,a in afaq) + '''
    </div>
  </div>
</section>
</main>
''' + cta_band("Tell us where you are and what you need") + footer()
write("service-areas-uganda.html", ar)

# ================================================================== 404
write("404.html", head("Page not found | A5 Systems Uganda","Page not found.","404.html",noindex=True,ads=False) + header("") + f'''<main id="main">
<section class="section"><div class="wrap" style="text-align:center;max-width:680px">
<h1>Page not found</h1>
<p>Sorry, that page does not exist or has moved. Try one of these instead.</p>
<div class="btn-row" style="justify-content:center"><a class="btn" href="index.html">Home</a><a class="btn btn-ghost" href="services.html">Services</a><a class="btn btn-ghost" href="contact.html">Contact us</a></div>
</div></section>
</main>
''' + footer())

# ================================================================== xindex (stale draft) stays noindex
x = open(os.path.join(ROOT,"xindex.html"),encoding="utf-8").read()
if 'noindex' not in x:
    x = x.replace('<meta name="viewport"', '<meta name="robots" content="noindex, follow">\n  <link rel="canonical" href="https://afive.cc/">\n  <meta name="viewport"',1)
    write("xindex.html", x)

# ================================================================== sitemap / robots
pages = ["index.html","services.html"] + list(S) + list(S2) + ["service-areas-uganda.html","Monitoring.html","products.html","about.html","contact.html","privacy.html"]
prio = {"index.html":"1.0","services.html":"0.9","contact.html":"0.8","Monitoring.html":"0.8","privacy.html":"0.3"}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in pages:
    loc = SITE + "/" + ("" if p=="index.html" else p)
    sm += f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio.get(p,'0.7')}</priority>\n  </url>\n"
sm += "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /xindex.html\nDisallow: /404.html\n\nSitemap: {SITE}/sitemap.xml\n")

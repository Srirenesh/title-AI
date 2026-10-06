import { useState, type ReactNode } from "react";

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

const documents = [
  { type: "Quitclaim deed", date: "May 14, 2024", party: "Robert Jones → John Smith", ref: "2024-018492", accent: true },
  { type: "Warranty deed", date: "Aug 03, 2020", party: "Anna Moore → Robert Jones", ref: "2020-044107" },
  { type: "Deed of trust", date: "May 14, 2024", party: "John Smith / First National", ref: "2024-018493" },
];

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

export default function App() {
  const [activeNav, setActiveNav] = useState("Overview");
  const [query, setQuery] = useState("123 Main Street, Austin, TX");
  const [searched, setSearched] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState<(typeof documents)[number] | null>(null);
  const [selectedOrder, setSelectedOrder] = useState<(typeof orders)[number] | null>(null);
  const [exceptions, setExceptions] = useState(initialExceptions);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [toast, setToast] = useState("");
  const [orderFilter, setOrderFilter] = useState("");
  const [settings, setSettings] = useState({ email: true, exceptions: true, completion: false });

  function runSearch(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim()) {
      setSearched(true);
      setActiveNav("Property search");
      showToast("Property sources connected. Search started.");
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
          <section className="welcome">
            <div>
              <span className="ai-label"><Icon name="sparkles" size={14} /> AI-assisted research</span>
              <h2>Good morning, Alex.</h2>
              <p>Start a property search or continue reviewing today’s active orders.</p>
            </div>
            <div className="today-stat">
              <span>Today</span><strong>12</strong><small>reports processed</small>
            </div>
          </section>
        )}

        {!showGreeting && (
          <section className="page-intro">
            <span className="ai-label"><Icon name="sparkles" size={14} /> Connected property sources</span>
            <h2>Research a property</h2>
            <p>Enter any known detail. Verity will normalize the input and search across authorized sources.</p>
          </section>
        )}

        <form className="search-card" onSubmit={runSearch}>
          <div className="search-icon"><Icon name="search" size={21} /></div>
          <label>
            <span>Search by address, APN, owner, or order number</span>
            <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Enter property details..." autoFocus={!showGreeting && !searched} />
          </label>
          <button type="submit">Search property <Icon name="arrow" size={17} /></button>
        </form>

        {!searched && (
          <section className="empty-search">
            <span><Icon name="search" size={28} /></span>
            <h3>Ready to search</h3>
            <p>Try a street address, assessor parcel number, owner name, or existing order ID.</p>
            <div><button onClick={() => setQuery("123 Main Street, Austin, TX")}>Use sample property</button></div>
          </section>
        )}

        {searched && (
          <>
            <div className="section-heading">
              <div><h3>Active search</h3><p>Order #COS-24831 · Updated just now</p></div>
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
                  <h3>{query.split(",")[0] || "123 Main Street"}</h3>
                  <p className="location"><Icon name="pin" size={15} /> Austin, Travis County, TX 78701</p>
                  <div className="property-meta">
                    <div><span>APN</span><strong>123-456-789</strong></div>
                    <div><span>Current owner</span><strong>John Smith</strong></div>
                    <div><span>Search type</span><strong>Current owner</strong></div>
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

            <section className="evidence-card">
              <div className="card-title evidence-title">
                <div><h3>Chain of title & evidence</h3><p>Source documents are preserved for every result.</p></div>
                <span className="confidence"><Icon name="sparkles" size={14} /> High confidence</span>
              </div>
              <div className="document-list">
                {documents.map((doc, index) => (
                  <button className="document-row" key={doc.ref} onClick={() => setSelectedDocument(doc)}>
                    <span className={`document-icon ${doc.accent ? "accent" : ""}`}><Icon name="file" size={18} /></span>
                    <span className="doc-index">0{index + 1}</span>
                    <span className="doc-main"><strong>{doc.type}</strong><small>{doc.party}</small></span>
                    <span className="doc-date"><strong>{doc.date}</strong><small>Instrument {doc.ref}</small></span>
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
          {activeNav === "Orders" && renderOrders()}
          {activeNav === "Exceptions" && renderExceptions()}
          {activeNav === "Reports" && renderReports()}
          {activeNav === "Settings" && renderSettings()}
          {activeNav === "Help center" && renderHelp()}
        </div>
      </main>
      {(selectedDocument || selectedOrder) && (
        <div className="modal-backdrop" onMouseDown={() => { setSelectedDocument(null); setSelectedOrder(null); }}>
          <section className="detail-modal" onMouseDown={(event) => event.stopPropagation()} role="dialog" aria-modal="true">
            <button className="modal-close" onClick={() => { setSelectedDocument(null); setSelectedOrder(null); }} aria-label="Close">×</button>
            <span className="document-icon accent"><Icon name={selectedDocument ? "file" : "orders"} /></span>
            <p className="muted-label">{selectedDocument ? "Recorded document" : "Title order"}</p>
            <h2>{selectedDocument?.type || selectedOrder?.property}</h2>
            <p className="modal-subtitle">{selectedDocument?.party || `${selectedOrder?.id} · ${selectedOrder?.county}`}</p>
            <div className="modal-details">
              <div><span>{selectedDocument ? "Recording date" : "Current owner"}</span><strong>{selectedDocument?.date || selectedOrder?.owner}</strong></div>
              <div><span>{selectedDocument ? "Instrument number" : "Order status"}</span><strong>{selectedDocument?.ref || selectedOrder?.status}</strong></div>
              <div><span>Source verification</span><strong className="verified"><Icon name="check" size={14} /> Verified</strong></div>
            </div>
            <button className="primary-action full" onClick={() => { showToast(selectedDocument ? "Source document opened." : "Order workspace opened."); setSelectedDocument(null); setSelectedOrder(null); }}>Open full record</button>
          </section>
        </div>
      )}
      {toast && <div className="toast"><Icon name="check" size={16} /> {toast}</div>}
    </div>
  );
}

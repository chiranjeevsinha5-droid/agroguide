import { useMemo, useState } from 'react';
import {
  ArrowLeft, ArrowRight, Check, ChevronDown, Droplets, Leaf,
  Menu, Search, ShieldCheck, Sprout, Sun, Timer, Wheat, X, CircleHelp,
} from 'lucide-react';

type Page = 'home' | 'find' | 'guide' | 'about' | 'result';
type Question = 'location' | 'soil' | 'water' | 'rainfall' | 'season' | 'goal';
type Answers = { state: string; district: string; soil: string; water: string; rainfall: string; season: string; goal: string };

type Crop = {
  name: string; season: string; water: string; weather: string; soil: string;
  duration: string; image: string; description: string;
};

const heroImage = 'https://images.pexels.com/photos/12656535/pexels-photo-12656535.jpeg?auto=compress&cs=tinysrgb&h=650&w=940';
const images = {
  rice: 'https://images.pexels.com/photos/19239403/pexels-photo-19239403.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  wheat: 'https://images.pexels.com/photos/36826793/pexels-photo-36826793.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  maize: 'https://images.pexels.com/photos/5029646/pexels-photo-5029646.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  cotton: 'https://images.pexels.com/photos/4264828/pexels-photo-4264828.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  potato: 'https://images.pexels.com/photos/8369485/pexels-photo-8369485.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  tomato: 'https://images.pexels.com/photos/33872280/pexels-photo-33872280.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
  sugarcane: 'https://images.pexels.com/photos/11466855/pexels-photo-11466855.jpeg?auto=compress&cs=tinysrgb&h=650&w=940',
};

const crops: Crop[] = [
  { name: 'Rice', season: 'Kharif', water: 'High', weather: 'Warm', soil: 'Loamy / Clay', duration: '100–150 days', image: images.rice, description: 'A dependable choice for warm weather and fields with good water availability.' },
  { name: 'Wheat', season: 'Rabi', water: 'Moderate', weather: 'Cool', soil: 'Loamy / Clay', duration: '120–150 days', image: images.wheat, description: 'A popular winter crop that grows well in fertile, well-drained soil.' },
  { name: 'Maize', season: 'Kharif', water: 'Moderate', weather: 'Warm', soil: 'Loamy', duration: '90–120 days', image: images.maize, description: 'A flexible crop with a shorter harvest time and many market uses.' },
  { name: 'Cotton', season: 'Kharif', water: 'Moderate', weather: 'Warm', soil: 'Black / Loamy', duration: '160–180 days', image: images.cotton, description: 'Best suited to warm, sunny conditions and deep soil.' },
  { name: 'Potato', season: 'Rabi', water: 'Moderate', weather: 'Cool', soil: 'Sandy / Loamy', duration: '80–110 days', image: images.potato, description: 'A quick-growing crop that prefers loose soil and regular watering.' },
  { name: 'Tomato', season: 'Zaid', water: 'Moderate', weather: 'Warm', soil: 'Loamy', duration: '90–120 days', image: images.tomato, description: 'A good option for growers looking for a faster vegetable harvest.' },
  { name: 'Sugarcane', season: 'Annual', water: 'High', weather: 'Warm', soil: 'Loamy / Clay', duration: '10–18 months', image: images.sugarcane, description: 'A longer crop for land with reliable water through the year.' },
  { name: 'Chickpea', season: 'Rabi', water: 'Low', weather: 'Cool', soil: 'Sandy / Loamy', duration: '95–120 days', image: images.wheat, description: 'A hardy winter crop that needs less water once established.' },
  { name: 'Mustard', season: 'Rabi', water: 'Low', weather: 'Cool', soil: 'Loamy', duration: '110–140 days', image: heroImage, description: 'A low-water winter crop with steady local demand.' },
  { name: 'Groundnut', season: 'Kharif', water: 'Moderate', weather: 'Warm', soil: 'Sandy / Loamy', duration: '100–130 days', image: images.potato, description: 'Does well in light, loose soil with good drainage.' },
];

const steps: { id: Question; label: string }[] = [
  { id: 'location', label: 'Location' }, { id: 'soil', label: 'Soil type' }, { id: 'water', label: 'Water availability' }, { id: 'rainfall', label: 'Rainfall' }, { id: 'season', label: 'Farming season' }, { id: 'goal', label: 'Your goal' },
];

const initialAnswers: Answers = { state: 'Uttar Pradesh', district: 'Gautam Buddh Nagar', soil: '', water: '', rainfall: '', season: '', goal: '' };

function App() {
  const [page, setPage] = useState<Page>('home');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Answers>(initialAnswers);
  const [search, setSearch] = useState('');
  const go = (next: Page) => { setPage(next); setMobileOpen(false); window.scrollTo({ top: 0, behavior: 'smooth' }); };
  const update = (key: keyof Answers, value: string) => setAnswers((current) => ({ ...current, [key]: value }));
  const filteredCrops = useMemo(() => crops.filter((crop) => crop.name.toLowerCase().includes(search.toLowerCase())), [search]);

  return (
    <div className="app-shell">
      <header className="site-header">
        <button className="brand" onClick={() => go('home')} aria-label="Go to AgriGuide home"><span className="brand-mark"><Leaf size={19} fill="currentColor" /></span><span>AgriGuide</span></button>
        <button className="menu-toggle" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Toggle menu">{mobileOpen ? <X /> : <Menu />}</button>
        <nav className={mobileOpen ? 'main-nav mobile-visible' : 'main-nav'}>
          <button className={page === 'home' ? 'nav-link active' : 'nav-link'} onClick={() => go('home')}>Home</button>
          <button className={page === 'find' || page === 'result' ? 'nav-link active' : 'nav-link'} onClick={() => go('find')}>Find Crop</button>
          <button className={page === 'guide' ? 'nav-link active' : 'nav-link'} onClick={() => go('guide')}>Crop Guide</button>
          <button className={page === 'about' ? 'nav-link active' : 'nav-link'} onClick={() => go('about')}>About</button>
        </nav>
      </header>

      {page === 'home' && <Home onNavigate={go} />}
      {page === 'find' && <FindCrop step={step} setStep={setStep} answers={answers} update={update} onBack={() => go('home')} onResult={() => go('result')} />}
      {page === 'result' && <Result answers={answers} onTryAgain={() => { setStep(0); go('find'); }} onGuide={() => go('guide')} />}
      {page === 'guide' && <Guide search={search} setSearch={setSearch} crops={filteredCrops} />}
      {page === 'about' && <About onNavigate={go} />}

      <footer className="site-footer"><div className="footer-inner"><div className="footer-brand"><span className="brand-mark"><Leaf size={17} fill="currentColor" /></span><strong>AgriGuide</strong><p>Simple crop advice for better farming decisions.</p></div><div className="footer-links"><button onClick={() => go('find')}>Find Crop</button><button onClick={() => go('guide')}>Crop Guide</button><button onClick={() => go('about')}>About us</button></div><div className="footer-note">Made for farmers, with care.</div></div></footer>
    </div>
  );
}

function Home({ onNavigate }: { onNavigate: (page: Page) => void }) {
  return <main>
    <section className="hero">
      <div className="hero-copy"><p className="eyebrow">Simple steps. Better harvest.</p><h1>Choose the right<br /><span>crop for your land.</span></h1><p className="hero-text">Get simple crop recommendations based on your land, water availability and farming season.</p><div className="hero-actions"><button className="button primary" onClick={() => onNavigate('find')}>Find My Crop <ArrowRight size={17} /></button><button className="button secondary" onClick={() => onNavigate('guide')}>Explore Crops</button></div></div>
      <div className="hero-image"><img src="https://images.pexels.com/photos/19392425/pexels-photo-19392425.jpeg?auto=compress&cs=tinysrgb&h=650&w=940" alt="Indian farmer sowing seeds in a sunlit field" /></div>
    </section>
    <section className="feature-strip"><Feature icon={<Sprout />} title="Simple questions" text="No technical agricultural knowledge required." /><Feature icon={<Droplets />} title="Consider your resources" text="Recommendations consider water and land conditions." blue /><Feature icon={<Wheat />} title="Better crop decisions" text="Get suitable options before planting." /></section>
    <section className="home-guide"><div><p className="eyebrow">How it works</p><h2>Good decisions begin<br />with simple answers.</h2></div><p className="section-lede">Tell us a little about your farm. We will help you understand which crops may fit your land and plans best.</p><div className="mini-steps"><MiniStep number="01" title="Tell us about your farm" text="Choose your soil, water, rainfall and season." /><MiniStep number="02" title="See your best match" text="Get a clear recommendation and reason." /><MiniStep number="03" title="Plan with confidence" text="Explore other crops worth considering." /></div></section>
  </main>;
}

function Feature({ icon, title, text, blue = false }: { icon: React.ReactNode; title: string; text: string; blue?: boolean }) { return <div className="feature"><div className={blue ? 'feature-icon blue' : 'feature-icon'}>{icon}</div><div><h3>{title}</h3><p>{text}</p></div></div>; }
function MiniStep({ number, title, text }: { number: string; title: string; text: string }) { return <div className="mini-step"><span>{number}</span><div><h3>{title}</h3><p>{text}</p></div></div>; }

function FindCrop({ step, setStep, answers, update, onBack, onResult }: { step: number; setStep: (value: number) => void; answers: Answers; update: (key: keyof Answers, value: string) => void; onBack: () => void; onResult: () => void }) {
  const current = steps[step];
  const answerKey = current.id === 'location' ? null : current.id;
  const selectedAnswer = answerKey ? answers[answerKey] : '';
  const canContinue = current.id === 'location' ? Boolean(answers.state && answers.district) : Boolean(selectedAnswer);
  const options: Record<Exclude<Question, 'location'>, string[]> = { soil: ['Sandy', 'Clay', 'Loamy', 'Black soil', 'Red soil', 'Not sure'], water: ['Very low', 'Low', 'Moderate', 'Good', 'Very good'], rainfall: ['Less than 50 cm', '50–100 cm', 'More than 100 cm', 'I don’t know'], season: ['Kharif', 'Rabi', 'Zaid'], goal: ['Higher income', 'Less water', 'Easy to grow', 'Faster harvest', 'Better local demand'] };
  return <main className="form-page"><div className="page-heading"><button className="back-link" onClick={onBack}><ArrowLeft size={16} /> Back</button><p className="eyebrow">A few simple questions</p><h1>Tell us about your farm</h1><p>Answer a few simple questions to get the best crop recommendation.</p></div><div className="form-layout"><div className="step-list">{steps.map((item, index) => <div className={index === step ? 'step-item current' : index < step ? 'step-item done' : 'step-item'} key={item.id}><span>{index < step ? <Check size={14} /> : index + 1}</span><strong>{item.label}</strong></div>)}</div><section className="question-card"><div className="question-top"><span>Step {step + 1} of {steps.length}</span><div className="progress"><i style={{ width: `${((step + 1) / steps.length) * 100}%` }} /></div></div><div className="question-content"><p className="eyebrow">{step === 0 ? 'Location' : step === 3 ? 'Rainfall in cm' : 'Farm details'}</p><h2>{step === 0 ? 'Where is your farm located?' : step === 1 ? 'What type of soil do you have?' : step === 2 ? 'How much water is available?' : step === 3 ? 'How much rainfall does your farm get?' : step === 4 ? 'Which season are you farming in?' : 'What is most important to you?'}</h2><p className="question-hint">{step === 0 ? 'Select your state and district.' : step === 1 ? 'Choose the option that feels closest. Not sure is okay.' : step === 2 ? 'Think about the water you can access during the crop season.' : step === 3 ? 'Choose the usual rainfall for your farm, measured in centimetres (cm).' : step === 4 ? 'Choose the season when you plan to plant.' : 'Choose the result that matters most to your family.'}</p>{step === 0 ? <div className="select-grid"><SelectField label="State" value={answers.state} onChange={(value) => update('state', value)} options={['Uttar Pradesh', 'Maharashtra', 'Punjab', 'Gujarat', 'Kerala']} /><SelectField label="District" value={answers.district} onChange={(value) => update('district', value)} options={['Gautam Buddh Nagar', 'Lucknow', 'Kanpur Nagar', 'Varanasi', 'Agra']} /></div> : <div className="option-grid">{options[current.id as Exclude<Question, 'location'>].map((option) => <button className={selectedAnswer === option ? 'choice selected' : 'choice'} key={option} onClick={() => update(answerKey as keyof Answers, option)}><span className="choice-radio">{selectedAnswer === option && <i />}</span>{option}</button>)}</div>}</div><div className="question-footer"><span className="not-sure"><CircleHelp size={16} /> Not sure? That's okay.</span><div className="question-actions">{step > 0 && <button className="button ghost" onClick={() => setStep(step - 1)}><ArrowLeft size={16} /> Back</button>}{step < steps.length - 1 ? <button className="button primary" disabled={!canContinue} onClick={() => setStep(step + 1)}>Next <ArrowRight size={16} /></button> : <button className="button primary" disabled={!canContinue} onClick={onResult}>Find Best Crop <ArrowRight size={16} /></button>}</div></div></section></div></main>;
}

function SelectField({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: string[] }) { return <label className="select-field"><span>{label}</span><div><select value={value} onChange={(event) => onChange(event.target.value)}>{options.map((option) => <option key={option}>{option}</option>)}</select><ChevronDown size={16} /></div></label>; }

function Result({ answers, onTryAgain, onGuide }: { answers: Answers; onTryAgain: () => void; onGuide: () => void }) {
  const mainCrop = answers.season === 'Rabi' ? crops[1] : answers.water === 'Low' || answers.water === 'Very low' || answers.rainfall === 'Less than 50 cm' ? crops[7] : crops[0];
  const alternatives = mainCrop.name === 'Rice' ? [crops[2], crops[1], crops[4]] : [crops[2], crops[0], crops[8]];
  return <main className="result-page"><div className="page-heading compact"><button className="back-link" onClick={onTryAgain}><ArrowLeft size={16} /> Back</button><p className="eyebrow">Your farm, your next step</p><h1>Your recommended crop</h1><p>Based on your farm details, this may be a strong match for you.</p></div><section className="recommendation-card"><img src={mainCrop.image} alt={mainCrop.name} /><div className="recommendation-copy"><div className="recommendation-title"><div><p className="eyebrow">Recommended for you</p><h2>{mainCrop.name}</h2></div><span className="match-pill">Best match</span></div><p>We recommend {mainCrop.name.toLowerCase()} because your selected season, land type and available water are a good fit for this crop.</p><div className="details-grid"><Detail icon={<Leaf />} label="Suitable soil" value={mainCrop.soil} /><Detail icon={<Droplets />} label="Water requirement" value={mainCrop.water} /><Detail icon={<Sun />} label="Rainfall" value={answers.rainfall || 'Not sure'} /><Detail icon={<Timer />} label="Growing season" value={mainCrop.season} /><Detail icon={<Timer />} label="Approx. duration" value={mainCrop.duration} /></div></div></section><section className="why-section"><div><p className="eyebrow">Why this crop?</p><h2>A practical match for your farm.</h2></div><ul>{['Suitable for your selected season', `Works well with ${answers.soil || 'your selected'} soil`, `Water availability is ${answers.water ? answers.water.toLowerCase() : 'suitable'}`, `Rainfall is ${answers.rainfall ? answers.rainfall.toLowerCase() : 'not known'}`].map((reason) => <li key={reason}><span><Check size={14} /></span>{reason}</li>)}</ul></section><section className="alternatives"><div className="section-title-row"><div><p className="eyebrow">Keep your options open</p><h2>You can also consider</h2></div><button className="text-link" onClick={onGuide}>Explore crop guide <ArrowRight size={16} /></button></div><div className="alternative-grid">{alternatives.map((crop) => <CropSmall key={crop.name} crop={crop} />)}</div></section><div className="result-actions"><button className="button secondary" onClick={onTryAgain}>Try Again</button><button className="button primary" onClick={onGuide}>View Crop Guide <ArrowRight size={17} /></button></div></main>;
}
function Detail({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) { return <div className="detail"><span>{icon}</span><div><small>{label}</small><strong>{value}</strong></div></div>; }
function CropSmall({ crop }: { crop: Crop }) { return <article className="crop-small"><img src={crop.image} alt={crop.name} /><div><h3>{crop.name}</h3><span className="small-match">Good match</span><p>{crop.description}</p></div></article>; }

function Guide({ search, setSearch, crops: shownCrops }: { search: string; setSearch: (value: string) => void; crops: Crop[] }) { return <main className="guide-page"><div className="page-heading"><p className="eyebrow">A simpler crop library</p><h1>Crop guide</h1><p>Explore different crops and learn about their growing conditions.</p></div><label className="search-box"><Search size={18} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search crops..." /></label><div className="crop-grid">{shownCrops.map((crop) => <article className="crop-card" key={crop.name}><img src={crop.image} alt={crop.name} /><div className="crop-card-body"><h3>{crop.name}</h3><div className="crop-meta"><span>{crop.season}</span><i>•</i><span>{crop.water} water</span></div><p>{crop.description}</p><div className="crop-facts"><span><Droplets size={14} /> {crop.water}</span><span><Leaf size={14} /> {crop.soil}</span></div></div></article>)}</div>{shownCrops.length === 0 && <div className="empty-state">No crops found. Try a different name.</div>}</main>; }

function About({ onNavigate }: { onNavigate: (page: Page) => void }) { return <main className="about-page"><div className="about-hero"><div><p className="eyebrow">About AgriGuide</p><h1>Helpful advice should feel simple.</h1><p>AgriGuide is designed to help farmers make a confident first crop decision without needing technical soil reports or complicated charts.</p><button className="button primary" onClick={() => onNavigate('find')}>Find My Crop <ArrowRight size={17} /></button></div><div className="about-illustration"><Sprout size={72} /><div><strong>Land. Water. Season.</strong><span>Start with what you know.</span></div></div></div><div className="about-values"><Value icon={<CircleHelp />} title="Plain language" text="We use familiar words and clear choices, so the advice is easy to understand." /><Value icon={<ShieldCheck />} title="Practical guidance" text="Recommendations focus on the things farmers can see and manage on their farm." /><Value icon={<Leaf />} title="More confidence" text="Compare suitable options before you plant, and take the next step with clarity." /></div></main>; }
function Value({ icon, title, text }: { icon: React.ReactNode; title: string; text: string }) { return <div className="value"><span>{icon}</span><h3>{title}</h3><p>{text}</p></div>; }

export default App;

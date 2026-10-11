import React, { useState, useEffect } from 'react';
import { speechService } from '../services/speech';

export default function FarmerMode({
  crops,
  categories,
  batches,
  currentLang,
  languages,
  t,
  isRtl,
  onRegisterHarvest,
  onSelectBatchForTrace,
}) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedCropId, setSelectedCropId] = useState('TUR');
  const [farmerName, setFarmerName] = useState('Rajesh Kumar');
  const [farmName, setFarmName] = useState('Sahyadri Bio-Farms');
  const [location, setLocation] = useState('Wayanad, Kerala');
  const [variety, setVariety] = useState('Alleppey Finger');
  const [quantity, setQuantity] = useState(850);
  const [harvestDate, setHarvestDate] = useState(new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');
  
  // Voice Assistant State
  const [isListening, setIsListening] = useState(false);
  const [voiceTranscript, setVoiceTranscript] = useState('');
  const [voiceStatus, setVoiceStatus] = useState('');
  const [registeredBatch, setRegisteredBatch] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Selected crop details
  const selectedCrop = crops.find((c) => c.id === selectedCropId) || crops[0];

  // Update variety when crop changes
  useEffect(() => {
    if (selectedCrop) {
      setVariety(selectedCrop.variety_sample || 'Standard Certified');
    }
  }, [selectedCropId]);

  // Voice Recognition Handler
  const currentLangMeta = languages.find((l) => l.code === currentLang) || { speech_code: 'en-IN' };

  const startVoiceAssistance = () => {
    if (isListening) {
      speechService.stopSpeaking();
      setIsListening(false);
      return;
    }

    if (!speechService.isRecognitionSupported()) {
      alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    setIsListening(true);
    setVoiceStatus('Listening... Please speak your crop, quantity, and name.');

    const recognizer = speechService.createRecognizer({
      lang: currentLangMeta.speech_code || 'en-IN',
      onResult: ({ transcript, isFinal }) => {
        setVoiceTranscript(transcript);
        if (isFinal) {
          setIsListening(false);
          setVoiceStatus('Processing voice input...');

          // Parse spoken data
          const parsed = speechService.parseHarvestSpeech(transcript, crops);
          if (parsed.crop_id) {
            setSelectedCropId(parsed.crop_id);
          }
          if (parsed.harvest_qty_kg) {
            setQuantity(parsed.harvest_qty_kg);
          }

          const responseText = `${t.voice_registered_spoken || 'Heard'}: ${transcript}`;
          setVoiceStatus(responseText);
          speechService.speak(responseText, currentLangMeta.speech_code);
        }
      },
      onError: (err) => {
        setIsListening(false);
        setVoiceStatus(`Voice error: ${err}`);
      },
      onEnd: () => {
        setIsListening(false);
      },
    });

    if (recognizer) {
      try {
        recognizer.start();
      } catch (err) {
        setIsListening(false);
      }
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    if (!quantity || quantity <= 0) {
      setErrorMsg(t.error_positive_quantity || 'Please enter a valid harvest quantity greater than 0 kg.');
      return;
    }
    if (!farmerName.trim()) {
      setErrorMsg(t.error_farmer_required || 'Farmer name is required.');
      return;
    }

    setIsSubmitting(true);
    try {
      const payload = {
        crop_id: selectedCropId,
        farmer: farmerName.trim(),
        farm_name: farmName.trim() || `${farmerName}'s Organic Plot`,
        location: location.trim(),
        variety: variety.trim(),
        harvest_qty_kg: parseInt(quantity, 10),
        harvest_date: harvestDate,
        notes: notes.trim(),
      };

      const result = await onRegisterHarvest(payload);
      if (result && result.batch) {
        setRegisteredBatch(result.batch);
        // Voice speech feedback
        const confirmMsg = `${t.success_registered || 'Harvest registered successfully! Batch ID'}: ${result.batch.batch_id}`;
        speechService.speak(confirmMsg, currentLangMeta.speech_code);
      }
    } catch (err) {
      setErrorMsg(err.message || 'Failed to register harvest');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Filter crops by category
  const filteredCrops = selectedCategory === 'all'
    ? crops
    : crops.filter((c) => c.category_id === selectedCategory);

  return (
    <div className="flex flex-col gap-8 pb-16">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-primary-container via-primary-container/95 to-secondary/30 rounded-2xl p-6 text-white shadow-md flex flex-col md:flex-row md:items-center justify-between gap-6 border border-white/10">
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-secondary text-white font-mono text-[11px] uppercase tracking-wider">
              {t.mode_farmer || 'Multilingual Farmer Mode'}
            </span>
            <span className="text-white/40">|</span>
            <span className="text-white/80 text-xs">
              {t.voice_ready || 'Voice Assistant Ready'}
            </span>
          </div>
          <h1 className="font-headline text-2xl md:text-3xl font-bold tracking-tight">
            {t.welcome_farmer || 'Welcome to PhytoTrace Farmer Portal'}
          </h1>
          <p className="text-white/80 text-sm max-w-2xl">
            {t.farmer_subtitle || 'Register your botanical harvests easily with 1-click crop selection and multilingual voice assistance.'}
          </p>
        </div>

        {/* Big Voice Assistant Button */}
        <div className="flex flex-col items-center gap-2 bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/15">
          <button
            onClick={startVoiceAssistance}
            className={`w-14 h-14 rounded-full flex items-center justify-center transition-all shadow-lg ${
              isListening
                ? 'bg-red-500 animate-pulse text-white scale-110 ring-4 ring-red-300'
                : 'bg-secondary hover:bg-secondary/90 text-white hover:scale-105'
            }`}
            title="Click to speak harvest details"
          >
            <span className="material-symbols-outlined text-[28px]">
              {isListening ? 'graphic_eq' : 'mic'}
            </span>
          </button>
          <span className="font-mono text-xs text-white font-semibold text-center">
            {isListening ? (t.voice_listening || 'Listening...') : (t.voice_speak_btn || 'Speak Details')}
          </span>
          {voiceStatus && (
            <span className="text-[11px] text-white/90 text-center max-w-xs truncate">
              {voiceStatus}
            </span>
          )}
        </div>
      </div>

      {/* Main Grid: Crop Selection + Harvest Registration Form */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: 20-Crop Visual Catalog (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="font-headline text-xl font-bold text-on-surface">
                {t.select_crop_title || '1. Select Your Botanical Crop'}
              </h2>
              <p className="text-xs text-on-surface-variant">
                {t.crop_catalog_hint || 'Touch any crop card to auto-fill the harvest form'}
              </p>
            </div>

            {/* Category Filter Pills */}
            <div className="flex flex-wrap items-center gap-1.5">
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                    selectedCategory === cat.id
                      ? 'bg-secondary text-white shadow-sm'
                      : 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high'
                  }`}
                >
                  <span>{cat.icon || '🌿'} </span>
                  <span>{cat.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Crops Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 max-h-[560px] overflow-y-auto p-1">
            {filteredCrops.map((crop) => {
              const isSelected = crop.id === selectedCropId;
              return (
                <button
                  key={crop.id}
                  type="button"
                  onClick={() => setSelectedCropId(crop.id)}
                  className={`flex flex-col p-3 rounded-xl border text-left transition-all relative ${
                    isSelected
                      ? 'bg-secondary/10 border-secondary shadow-md ring-2 ring-secondary/30'
                      : 'bg-white border-outline-variant/50 hover:border-secondary/60 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">{crop.icon || '🌿'}</span>
                    <span className="font-mono text-[10px] font-bold px-1.5 py-0.5 rounded bg-surface-container text-on-surface-variant">
                      {crop.id}
                    </span>
                  </div>
                  <span className="font-headline text-sm font-bold text-on-surface leading-tight">
                    {crop.localized_name || crop.common_name}
                  </span>
                  {crop.localized_name !== crop.common_name && (
                    <span className="text-[11px] text-on-surface-variant/80 font-medium truncate">
                      {crop.common_name}
                    </span>
                  )}
                  <span className="text-[10px] text-outline font-mono italic mt-1 truncate">
                    {crop.scientific_name}
                  </span>
                  <span className="mt-2 text-[10px] font-mono px-2 py-0.5 rounded-full bg-surface-container-low text-secondary font-semibold w-max">
                    {crop.category_label || crop.category}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Harvest Registration Form (5 cols) */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-5">
          <div className="flex items-center justify-between border-b border-outline-variant/20 pb-3">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-secondary/10 text-secondary flex items-center justify-center">
                <span className="material-symbols-outlined text-[20px]">add_task</span>
              </span>
              <h2 className="font-headline text-lg font-bold text-on-surface">
                {t.farmer_register_harvest || '2. Register Harvest Batch'}
              </h2>
            </div>
            {selectedCrop && (
              <span className="font-mono text-xs font-semibold px-2.5 py-1 rounded-md bg-secondary text-white">
                {selectedCrop.icon} {selectedCrop.id}
              </span>
            )}
          </div>

          {errorMsg && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg flex items-center gap-2">
              <span className="material-symbols-outlined text-[16px]">error</span>
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Success Banner */}
          {registeredBatch && (
            <div className="p-4 bg-emerald-50 border border-emerald-300 text-emerald-900 rounded-xl flex flex-col gap-2 animate-fadeIn">
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm flex items-center gap-1.5 text-emerald-800">
                  <span className="material-symbols-outlined text-[18px]">verified</span>
                  <span>{t.success_registered || 'Harvest Registered!'}</span>
                </span>
                <span className="font-mono text-xs font-bold bg-emerald-200 px-2 py-0.5 rounded text-emerald-900">
                  {registeredBatch.batch_id}
                </span>
              </div>
              <p className="text-xs text-emerald-700">
                {registeredBatch.botanical} ({registeredBatch.harvest_qty_kg} kg) logged into property graph.
              </p>
              <button
                type="button"
                onClick={() => onSelectBatchForTrace(registeredBatch.batch_id)}
                className="mt-1 text-xs font-semibold text-emerald-800 hover:text-emerald-950 underline text-left flex items-center gap-1"
              >
                <span>{t.view_trace_journey || 'View 10-Tier Custody Journey'}</span>
                <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
            </div>
          )}

          <form onSubmit={handleFormSubmit} className="flex flex-col gap-4 text-xs font-medium">
            {/* Selected Crop Badge */}
            <div className="bg-surface-container-low p-3 rounded-xl border border-outline-variant/30 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-on-surface-variant block uppercase font-mono">
                  {t.selected_botanical || 'Selected Botanical'}
                </span>
                <span className="font-headline text-base font-bold text-on-surface">
                  {selectedCrop?.localized_name || selectedCrop?.common_name}
                </span>
                <span className="text-[11px] text-outline italic ml-2">
                  ({selectedCrop?.scientific_name})
                </span>
              </div>
              <span className="text-2xl">{selectedCrop?.icon}</span>
            </div>

            {/* Variety */}
            <div className="flex flex-col gap-1">
              <label className="text-on-surface font-semibold">
                {t.variety_label || 'Cultivar / Variety'}
              </label>
              <input
                type="text"
                value={variety}
                onChange={(e) => setVariety(e.target.value)}
                className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs focus:outline-none focus:border-secondary focus:bg-white"
                placeholder="e.g. Alleppey Finger, Krishna Tulsi"
              />
            </div>

            {/* Farmer Name & Farm Name */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="flex flex-col gap-1">
                <label className="text-on-surface font-semibold">
                  {t.farmer_name_label || 'Farmer Name'} *
                </label>
                <input
                  type="text"
                  required
                  value={farmerName}
                  onChange={(e) => setFarmerName(e.target.value)}
                  className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs focus:outline-none focus:border-secondary focus:bg-white"
                />
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-on-surface font-semibold">
                  {t.farm_name_label || 'Farm Name / Grove'} *
                </label>
                <input
                  type="text"
                  required
                  value={farmName}
                  onChange={(e) => setFarmName(e.target.value)}
                  className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs focus:outline-none focus:border-secondary focus:bg-white"
                />
              </div>
            </div>

            {/* Location */}
            <div className="flex flex-col gap-1">
              <label className="text-on-surface font-semibold">
                {t.location_label || 'Origin Location'} *
              </label>
              <input
                type="text"
                required
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs focus:outline-none focus:border-secondary focus:bg-white"
                placeholder="District, State"
              />
            </div>

            {/* Quantity & Date */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="flex flex-col gap-1">
                <label className="text-on-surface font-semibold">
                  {t.harvest_qty_label || 'Harvest Quantity (kg)'} *
                </label>
                <input
                  type="number"
                  required
                  min="1"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs font-mono font-semibold focus:outline-none focus:border-secondary focus:bg-white"
                />
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-on-surface font-semibold">
                  {t.harvest_date_label || 'Harvest Date'} *
                </label>
                <input
                  type="date"
                  required
                  value={harvestDate}
                  onChange={(e) => setHarvestDate(e.target.value)}
                  className="h-10 px-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs font-mono focus:outline-none focus:border-secondary focus:bg-white"
                />
              </div>
            </div>

            {/* Notes */}
            <div className="flex flex-col gap-1">
              <label className="text-on-surface font-semibold">
                {t.notes_label || 'Harvest Condition / Notes'}
              </label>
              <textarea
                rows="2"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="p-3 bg-surface-container-low border border-outline-variant/50 rounded-lg text-on-surface text-xs focus:outline-none focus:border-secondary focus:bg-white"
                placeholder="Moisture level, solar drying method, organic compost..."
              />
            </div>

            {/* Big Primary Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 w-full h-12 bg-secondary hover:bg-secondary/90 text-white font-headline font-bold text-sm rounded-xl shadow-md flex items-center justify-center gap-2 transition disabled:opacity-50"
            >
              <span className="material-symbols-outlined text-[20px]">check_circle</span>
              <span>
                {isSubmitting
                  ? (t.saving_btn || 'Registering in Graph...')
                  : (t.save_register_btn || 'Save & Register Harvest')}
              </span>
            </button>
          </form>
        </div>
      </div>

      {/* Farmer's Recent Batches Section */}
      <div className="bg-white p-6 rounded-2xl border border-outline-variant/40 shadow-sm flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-secondary text-[22px]">history_edu</span>
            <h2 className="font-headline text-lg font-bold text-on-surface">
              {t.farmer_my_batches || 'My Registered Harvests & Live Status'}
            </h2>
          </div>
          <span className="font-mono text-xs text-on-surface-variant">
            {batches.length} {t.batches_logged || 'Batches in System'}
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-outline-variant/30 text-on-surface-variant uppercase font-mono text-[10px]">
                <th className="py-2.5 px-3">Batch ID</th>
                <th className="py-2.5 px-3">Botanical Crop</th>
                <th className="py-2.5 px-3">Farmer & Farm</th>
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3">Yield (kg)</th>
                <th className="py-2.5 px-3">Stage</th>
                <th className="py-2.5 px-3">Verification</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/15">
              {batches.slice(0, 8).map((b) => (
                <tr key={b.batch_id} className="hover:bg-surface-container-low transition">
                  <td className="py-3 px-3 font-mono font-bold text-secondary">
                    {b.batch_id}
                  </td>
                  <td className="py-3 px-3 font-semibold text-on-surface">
                    {b.botanical}
                    <span className="text-[10px] text-outline block italic">
                      {b.scientific_name}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-on-surface font-medium block">{b.farmer}</span>
                    <span className="text-[11px] text-on-surface-variant block">{b.farm_name}</span>
                  </td>
                  <td className="py-3 px-3 font-mono text-on-surface-variant">
                    {b.harvest_date}
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-on-surface">
                    {b.harvest_qty_kg} kg
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded font-mono text-[10px] bg-surface-container text-on-surface font-semibold">
                      {b.current_stage || 'Harvest Batch'}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span
                      className={`px-2 py-0.5 rounded font-mono text-[10px] font-semibold ${
                        b.status === 'Verified'
                          ? 'bg-emerald-100 text-emerald-800'
                          : b.status === 'In Transit'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}
                    >
                      {b.status}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <button
                      onClick={() => onSelectBatchForTrace(b.batch_id)}
                      className="px-2.5 py-1 bg-secondary/10 hover:bg-secondary text-secondary hover:text-white rounded-lg text-xs font-semibold transition flex items-center gap-1 ml-auto"
                    >
                      <span className="material-symbols-outlined text-[14px]">account_tree</span>
                      <span>Trace</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

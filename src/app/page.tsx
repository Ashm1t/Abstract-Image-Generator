// Welcome to the Abstract Art Generator! 🎨
// This is where the magic happens - beautiful blue glass UI meets AI art generation

'use client';

import { useState, useRef, useEffect } from 'react';

interface StyleInfo {
  id: number;
  name: string;
  description: string;
  characteristics: string;
  dominantColor: string;
  contrastLevel: string;
  contrastValue: number;
}

interface VariationType {
  id: string;
  name: string;
  description: string;
}

// 🎭 These are our 5 magical ways to create art variations
const VARIATION_TYPES: VariationType[] = [
  { id: 'blend', name: 'Blend', description: 'Smooth transitions between similar artworks' },
  { id: 'filter', name: 'Filter', description: 'Enhances style-specific characteristics' },
  { id: 'color_morph', name: 'Color Morph', description: 'Morphs colors between artworks' },
  { id: 'cross_cluster', name: 'Cross-Style', description: 'Creates hybrids between different styles' },
  { id: 'mixed', name: 'Mixed', description: 'Random combination of all types' }
];

// 🎨 Our 15 discovered art styles - each one has its own personality!
const STYLE_INFO: StyleInfo[] = [
  { id: 0, name: "Balanced Neutral", description: "Clean balanced forms with neutral tones", characteristics: "Balanced, neutral", dominantColor: "Red-warm", contrastLevel: "Medium", contrastValue: 40.7 },
  { id: 1, name: "Warm Earth", description: "Earthy and warm compositions", characteristics: "Warm, earthy", dominantColor: "Red-warm", contrastLevel: "Low", contrastValue: 36.6 },
  { id: 2, name: "Cool Flow", description: "Flowing forms with cool tones", characteristics: "Cool, flowing", dominantColor: "Green", contrastLevel: "Lowest", contrastValue: 31.7 },
  { id: 3, name: "High Balance", description: "High contrast balanced compositions", characteristics: "Neutral, balanced", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 56.5 },
  { id: 4, name: "Light Bright", description: "Light and bright compositions", characteristics: "Light, bright", dominantColor: "Red-warm", contrastLevel: "Low", contrastValue: 36.6 },
  { id: 5, name: "Cool Minimal", description: "Minimalist designs with cool tones", characteristics: "Cool, minimal", dominantColor: "Blue", contrastLevel: "Low", contrastValue: 34.5 },
  { id: 6, name: "High Drama", description: "Dramatic high contrast works", characteristics: "High contrast", dominantColor: "Red-warm", contrastLevel: "Highest", contrastValue: 83.1 },
  { id: 7, name: "Warm Texture", description: "Textured works with warm tones", characteristics: "Warm, textured", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 60.3 },
  { id: 8, name: "Dark Mood", description: "Moody compositions with dark tones", characteristics: "Dark, moody", dominantColor: "Red-warm", contrastLevel: "Medium", contrastValue: 43.9 },
  { id: 9, name: "Warm Express", description: "Expressive works with warm colors", characteristics: "Warm, expressive", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 56.4 },
  { id: 10, name: "Earth Ground", description: "Grounded works with earthy tones", characteristics: "Earthy, grounded", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 58.7 },
  { id: 11, name: "Bright Dynamic", description: "Dynamic compositions with bright colors", characteristics: "Bright, dynamic", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 62.6 },
  { id: 12, name: "Subtle Mute", description: "Subtle works with muted tones", characteristics: "Muted, subtle", dominantColor: "Red-warm", contrastLevel: "Medium", contrastValue: 44.1 },
  { id: 13, name: "Cool Structure", description: "Structured works with cool colors", characteristics: "Cool, structured", dominantColor: "Green", contrastLevel: "Medium", contrastValue: 46.6 },
  { id: 14, name: "Dark Intense", description: "Intense works with dark tones", characteristics: "Dark, intense", dominantColor: "Red-warm", contrastLevel: "High", contrastValue: 58.8 }
];

export default function Home() {
  // 🎛️ Our app's state - keeping track of what the user wants to create
  const [isCreatingArt, setIsCreatingArt] = useState(false); // Are we currently generating? 
  const [chosenStyle, setChosenStyle] = useState<number>(0); // Which art style did they pick?
  const [chosenVariation, setChosenVariation] = useState<string>('mixed'); // What kind of variation?
  const [latestArtwork, setLatestArtwork] = useState<string | null>(null); // The masterpiece we just created
  const [oopsMessage, setOopsMessage] = useState<string | null>(null); // If something goes wrong

  // 🎨 This is where the magic happens - calling our AI art generator!
  const createMasterpiece = async () => {
    setIsCreatingArt(true);
    setOopsMessage(null);
    
    try {
      // 📞 Calling our backend to work its magic
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          style: chosenStyle,
          variationType: chosenVariation,
          seed: Math.floor(Math.random() * 10000) // A bit of randomness for uniqueness
        }),
      });

      const result = await response.json();
      
      if (result.success) {
        setLatestArtwork(result.imagePath); // 🎉 Success! Show the beautiful art
      } else {
        setOopsMessage(result.error || 'Something went wrong with the art creation');
      }
    } catch (err) {
      setOopsMessage('Hmm, looks like we lost connection. Try again?');
    } finally {
      setIsCreatingArt(false); // We're done, regardless of success or failure
    }
  };

  // 🎭 Get info about the currently selected style and variation
  const currentStyleInfo = STYLE_INFO[chosenStyle];
  const currentVariationInfo = VARIATION_TYPES.find(v => v.id === chosenVariation);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 relative overflow-hidden">
      {/* ✨ Beautiful animated background - like floating in space */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-400/5 rounded-full blur-3xl animate-slow-spin"></div>
      </div>

      {/* 🌟 Glass overlay pattern - gives that beautiful reflective effect */}
      <div className="absolute inset-0 opacity-30">
        <div className="h-full w-full bg-gradient-to-br from-blue-400/20 via-transparent to-cyan-400/20"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.1),transparent_50%)]"></div>
      </div>

      <div className="relative z-10 min-h-screen flex flex-col">
        {/* 🎪 Header - Welcome to our art studio! */}
        <header className="p-8 text-center">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-blue-200 via-cyan-200 to-blue-300 bg-clip-text text-transparent mb-4 tracking-wide">
            Abstract Art Generator
          </h1>
          <p className="text-blue-200/80 text-xl font-light tracking-wider">
            Instant Style-Based Art Creation
          </p>
        </header>

        <div className="flex-1 flex flex-col lg:flex-row gap-8 p-8 max-w-7xl mx-auto w-full">
          {/* 🎛️ Left Panel - Your creative control center */}
          <div className="lg:w-1/3 space-y-6">
            {/* 🎨 Style Selection - Pick your artistic vibe */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-semibold text-blue-100 mb-4 flex items-center gap-3">
                <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse"></div>
                Art Style Selection
              </h2>
              
              <div className="space-y-4">
                <select
                  value={chosenStyle}
                  onChange={(e) => setChosenStyle(Number(e.target.value))}
                  className="w-full bg-blue-900/50 backdrop-blur-sm border border-blue-400/30 rounded-lg px-4 py-3 text-blue-100 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 transition-all duration-300"
                >
                  {STYLE_INFO.map((style) => (
                    <option key={style.id} value={style.id} className="bg-blue-900">
                      {style.name}
                    </option>
                  ))}
                </select>

                {/* 📊 Style Info - Learn about your chosen style */}
                <div className="bg-blue-950/30 backdrop-blur-sm rounded-lg p-4 border border-blue-400/20">
                  <h3 className="text-lg font-medium text-cyan-200 mb-2">{currentStyleInfo.name}</h3>
                  <p className="text-blue-200/80 text-sm mb-3">{currentStyleInfo.description}</p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="text-blue-300/70">
                      <span className="font-medium">Characteristics:</span><br/>
                      {currentStyleInfo.characteristics}
                    </div>
                    <div className="text-blue-300/70">
                      <span className="font-medium">Color:</span><br/>
                      {currentStyleInfo.dominantColor}
                    </div>
                    <div className="text-blue-300/70">
                      <span className="font-medium">Contrast:</span><br/>
                      {currentStyleInfo.contrastLevel} ({currentStyleInfo.contrastValue})
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 🎲 Variation Type Selection - How should we remix it? */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-semibold text-blue-100 mb-4 flex items-center gap-3">
                <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
                Variation Type
              </h2>
              
              <div className="space-y-4">
                <select
                  value={chosenVariation}
                  onChange={(e) => setChosenVariation(e.target.value)}
                  className="w-full bg-blue-900/50 backdrop-blur-sm border border-blue-400/30 rounded-lg px-4 py-3 text-blue-100 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 transition-all duration-300"
                >
                  {VARIATION_TYPES.map((type) => (
                    <option key={type.id} value={type.id} className="bg-blue-900">
                      {type.name}
                    </option>
                  ))}
                </select>

                {/* 💡 Variation Info - What will this do? */}
                <div className="bg-blue-950/30 backdrop-blur-sm rounded-lg p-4 border border-blue-400/20">
                  <p className="text-blue-200/80 text-sm">
                    {currentVariationInfo?.description}
                  </p>
                </div>
              </div>
            </div>

            {/* 🚀 The Big Red Button (well, blue in this case) */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
              <button
                onClick={createMasterpiece}
                disabled={isCreatingArt}
                className={`
                  w-full py-4 px-6 rounded-xl text-white font-medium text-lg tracking-wide transition-all duration-300 transform
                  ${isCreatingArt 
                    ? 'bg-gray-600/50 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 hover:scale-105 shadow-lg hover:shadow-cyan-500/25'
                  }
                `}
              >
                {isCreatingArt ? (
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Creating your masterpiece...
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-5 h-5 bg-cyan-400 rounded-full animate-pulse"></div>
                    Generate New Art
                  </div>
                )}
              </button>
              
              {/* 😅 If something goes wrong, we'll let you know gently */}
              {oopsMessage && (
                <div className="mt-4 p-3 bg-red-500/20 border border-red-400/30 rounded-lg text-red-200 text-sm">
                  {oopsMessage}
                </div>
              )}
            </div>

            {/* 📊 System Status - Everything looking good? */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 shadow-2xl">
              <h3 className="text-lg font-medium text-blue-100 mb-3 flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                System Status
              </h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-blue-200/80">
                  <span>Generator:</span>
                  <span className="text-green-300">Ready to create!</span>
                </div>
                <div className="flex justify-between text-blue-200/80">
                  <span>Art Styles:</span>
                  <span className="text-cyan-300">15 unique styles</span>
                </div>
                <div className="flex justify-between text-blue-200/80">
                  <span>Speed:</span>
                  <span className="text-cyan-300">~2 seconds ⚡</span>
                </div>
              </div>
            </div>
          </div>

          {/* 🖼️ Right Panel - Where your art comes to life */}
          <div className="lg:w-2/3 flex flex-col">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl flex-1 flex flex-col items-center justify-center min-h-[600px]">
              {latestArtwork ? (
                // 🎉 Ta-da! Your beautiful artwork is ready
                <div className="text-center space-y-4">
                  <h3 className="text-2xl font-medium text-blue-100 mb-6">Your Masterpiece is Ready! 🎨</h3>
                  <div className="relative group">
                    <img
                      src={latestArtwork}
                      alt={`Your generated ${currentStyleInfo.name} artwork`}
                      className="max-w-full max-h-[500px] rounded-lg shadow-2xl border border-blue-400/20 transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 rounded-lg bg-gradient-to-t from-blue-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  <div className="text-blue-200/80 text-sm space-y-1">
                    <p>Style: <span className="text-cyan-300 font-medium">{currentStyleInfo.name}</span></p>
                    <p>Variation: <span className="text-purple-300 font-medium">{currentVariationInfo?.name}</span></p>
                  </div>
                </div>
              ) : (
                // 👋 Welcome screen - ready to start creating
                <div className="text-center space-y-6">
                  <div className="w-32 h-32 mx-auto bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-2xl flex items-center justify-center border border-blue-400/30">
                    <div className="w-16 h-16 border-2 border-blue-400/50 border-dashed rounded-lg flex items-center justify-center">
                      <svg className="w-8 h-8 text-blue-400/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-2xl font-medium text-blue-100 mb-2">Ready to Create Art? ✨</h3>
                    <p className="text-blue-200/70">Pick a style, choose a variation type, and let's make something beautiful together!</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 🎭 A little CSS magic for our slow-spinning background element */}
      <style jsx global>{`
        @keyframes slow-spin {
          from { transform: translate(-50%, -50%) rotate(0deg); }
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .animate-slow-spin {
          animation: slow-spin 60s linear infinite;
        }
      `}</style>
    </div>
  );
} 
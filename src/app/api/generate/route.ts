import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const { style, variationType = 'mixed', seed } = await request.json();
    
    if (style === undefined || style < 0 || style > 14) {
      return NextResponse.json({ error: 'Invalid style. Must be between 0 and 14.' }, { status: 400 });
    }

    // Call Python script for variation generation
    const scriptPath = path.join(process.cwd(), 'src', 'scripts', 'generate_variations.py');
    const outputDir = path.join(process.cwd(), 'public', 'generated');
    
    console.log('🎨 Starting art generation...');
    console.log('Script path:', scriptPath);
    console.log('Output dir:', outputDir);
    console.log('Style:', style, 'Variation:', variationType, 'Seed:', seed);
    
    return new Promise((resolve) => {
      const python = spawn('python', [
        scriptPath,
        '--num_variations', '1',
        '--variation_type', variationType,
        '--style', style.toString(),
        '--seed', (seed || Math.floor(Math.random() * 10000)).toString(),
        '--output_dir', outputDir
      ]);

      let stdout = '';
      let stderr = '';

      python.stdout.on('data', (data) => {
        const output = data.toString();
        stdout += output;
        console.log('Python stdout:', output.trim());
      });

      python.stderr.on('data', (data) => {
        const error = data.toString();
        stderr += error;
        console.error('Python stderr:', error.trim());
      });

      python.on('close', (code) => {
        console.log('Python process finished with code:', code);
        console.log('Full stdout:', stdout);
        console.log('Full stderr:', stderr);
        
        if (code === 0) {
          try {
            // Parse the output to get the generated image path
            const lines = stdout.trim().split('\n');
            console.log('Output lines:', lines);
            
            // Find the line with the generated file path
            let imagePath = '';
            for (const line of lines) {
              if (line.includes('.png') && (line.includes('public') || line.includes('generated'))) {
                // Extract just the filename and path from public/generated onwards
                const match = line.match(/generated[\\\/]([^\\\/]+\.png)/);
                if (match) {
                  imagePath = '/generated/' + match[1];
                  break;
                }
              }
            }
            
            console.log('Extracted image path:', imagePath);
            
            if (!imagePath) {
              resolve(NextResponse.json({ 
                error: 'Could not find generated image path',
                details: stdout,
                lines: lines
              }, { status: 500 }));
              return;
            }
            
            resolve(NextResponse.json({ 
              success: true, 
              imagePath: imagePath,
              style: style,
              variationType: variationType
            }));
          } catch (e) {
            console.error('Error parsing output:', e);
            resolve(NextResponse.json({ 
              error: 'Failed to parse generation output',
              details: stdout,
              parseError: e instanceof Error ? e.message : 'Unknown parse error'
            }, { status: 500 }));
          }
        } else {
          resolve(NextResponse.json({ 
            error: 'Art generation failed', 
            details: stderr,
            stdout: stdout,
            exitCode: code
          }, { status: 500 }));
        }
      });

      python.on('error', (error) => {
        console.error('Python spawn error:', error);
        resolve(NextResponse.json({ 
          error: 'Failed to start Python process', 
          details: error.message 
        }, { status: 500 }));
      });
    });

  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json({ 
      error: 'Internal server error', 
      details: error instanceof Error ? error.message : 'Unknown error' 
    }, { status: 500 });
  }
} 
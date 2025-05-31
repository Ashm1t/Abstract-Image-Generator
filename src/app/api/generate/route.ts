import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

// Helper function to run Python script
async function runPythonScript(style: number, variationType: string, seed?: number): Promise<string> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(process.cwd(), 'src', 'scripts', 'generate_variations.py');
    const outputDir = path.join(process.cwd(), 'public', 'generated');
    
    const args = [
      scriptPath,
      '--style', style.toString(),
      '--variation', variationType,
      '--output-dir', outputDir,
      '--num-variations', '1'
    ];
    
    if (seed !== undefined) {
      args.push('--seed', seed.toString());
    }

    const pythonProcess = spawn('python', args);
    let outputPath = '';

    pythonProcess.stdout.on('data', (data) => {
      const output = data.toString();
      if (output.includes('public\\generated\\')) {
        outputPath = output.trim().split('public\\generated\\')[1];
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code === 0 && outputPath) {
        resolve(outputPath.trim());
      } else {
        reject(new Error(`Python process exited with code ${code}`));
      }
    });
  });
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { style, variationType, seed } = body;

    if (style === undefined || !variationType) {
      return NextResponse.json(
        { error: 'Missing required parameters' },
        { status: 400 }
      );
    }

    const imagePath = await runPythonScript(style, variationType, seed);
    
    return NextResponse.json({
      success: true,
      imagePath: `/generated/${imagePath}`
    });

  } catch (error) {
    console.error('Error generating art:', error);
    return NextResponse.json(
      { error: 'Failed to generate art' },
      { status: 500 }
    );
  }
}

// GET method to check API health
export async function GET() {
  return NextResponse.json({ status: 'Art generation API is running' });
} 
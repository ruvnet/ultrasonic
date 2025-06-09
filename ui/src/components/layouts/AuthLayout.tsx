import { Outlet } from 'react-router-dom'
import { RadioIcon } from 'lucide-react'

export function AuthLayout() {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Auth form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          <div className="mb-8 flex items-center justify-center">
            <RadioIcon className="h-12 w-12 text-primary" />
            <h1 className="ml-3 text-2xl font-bold">Ultrasonic Agentics</h1>
          </div>
          <Outlet />
        </div>
      </div>

      {/* Right side - Image/Pattern */}
      <div className="hidden lg:block relative flex-1">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-primary/30" />
        <div className="absolute inset-0 bg-[url('/wave-pattern.svg')] bg-cover bg-center opacity-10" />
        <div className="relative h-full flex items-center justify-center p-12">
          <div className="max-w-md text-center">
            <h2 className="text-3xl font-bold text-primary mb-4">
              Secure Command Embedding
            </h2>
            <p className="text-muted-foreground">
              Embed and decode encrypted commands in audio and video files using 
              ultrasonic steganography. Military-grade encryption meets cutting-edge 
              audio processing technology.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
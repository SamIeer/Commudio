import { Loader2 } from 'lucide-react';

const Loader = ({ size = 'md', text = '' }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <Loader2 className={`${sizes[size]} text-primary-600 animate-spin`} />
      {text && <p className="mt-4 text-sm text-gray-600">{text}</p>}
    </div>
  );
};

export default Loader;
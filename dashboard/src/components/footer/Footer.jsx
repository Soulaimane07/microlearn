export default function Footer() {
  return (
    <footer className="w-full border-t border-gray-300 bg-gray-100 py-4 px-6 text-gray-600 flex items-center justify-between mt-auto">
      <p className="text-sm">
        © {new Date().getFullYear()} <span className="font-semibold">MicroLearn</span>. All rights reserved.
      </p>

      <div className="flex items-center gap-4 text-sm">
        <a href="#" className="hover:text-gray-900 transition">Docs</a>
        <a href="#" className="hover:text-gray-900 transition">Support</a>
        <a href="#" className="hover:text-gray-900 transition">Privacy</a>
      </div>
    </footer>
  );
}

import React from 'react';
import Link from '@docusaurus/Link';
import { Github, Twitter, Linkedin, Mail, BookOpen, Code, Cpu, Zap, ExternalLink } from 'lucide-react';

export default function Footer(): JSX.Element {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    book: [
      { label: 'Get Started', to: '/docs/intro' },
      { label: 'Module 1: ROS 2', to: '/docs/module-1' },
      { label: 'Module 2: Simulation', to: '/docs/module-2' },
      { label: 'Module 3: AI & RL', to: '/docs/module-3' },
      { label: 'Module 4: Voice Control', to: '/docs/module-4' },
    ],
    resources: [
      { label: 'ROS 2 Documentation', href: 'https://docs.ros.org/', external: true },
      { label: 'Gazebo', href: 'https://gazebosim.org/', external: true },
      { label: 'NVIDIA Isaac Sim', href: 'https://developer.nvidia.com/isaac-sim', external: true },
      { label: 'OpenAI Whisper', href: 'https://openai.com/research/whisper', external: true },
    ],
    learn: [
      { label: 'ROS 2 Basics', to: '/docs/module-1' },
      { label: 'Gazebo Simulation', to: '/docs/module-2' },
      { label: 'Navigation Stack', to: '/docs/module-2/chapter-2-6-nav2' },
      { label: 'AI Integration', to: '/docs/module-3' },
    ],
  };

  const socialLinks = [
    { icon: Github, href: 'https://github.com/muzaffar401', label: 'GitHub' },
    { icon: Twitter, href: 'https://twitter.com', label: 'Twitter' },
    { icon: Linkedin, href: 'https://linkedin.com', label: 'LinkedIn' },
    { icon: Mail, href: 'mailto:contact@example.com', label: 'Email' },
  ];

  return (
    <footer className="relative bg-white dark:bg-gradient-to-b dark:from-slate-900 dark:via-slate-950 dark:to-slate-950 border-t border-slate-300 dark:border-slate-800/50 shadow-lg dark:shadow-none">
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-slate-50 to-transparent dark:from-blue-950/20 pointer-events-none"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12 mb-12">
          {/* Brand Column */}
          <div className="lg:col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">Physical AI & Humanoid Robotics</h3>
            </div>
            <p className="text-slate-600 dark:text-slate-400 text-sm leading-relaxed mb-6">
              Master ROS 2, build intelligent robots, and create the future of autonomous systems.
            </p>
            {/* Social Links */}
            <div className="flex gap-3">
              {socialLinks.map((social, index) => {
                const Icon = social.icon;
                return (
                  <a
                    key={index}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 bg-slate-100 dark:bg-slate-800/50 hover:bg-slate-200 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700/50 hover:border-blue-500/50 dark:hover:border-blue-500/50 rounded-lg transition-all duration-300 hover:scale-110 group"
                    aria-label={social.label}>
                    <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Book Links */}
          <div>
            <h4 className="text-slate-900 dark:text-white font-semibold mb-4 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              Book
            </h4>
            <ul className="space-y-3">
              {footerLinks.book.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.to}
                    className="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm transition-colors duration-200 flex items-center gap-1 group">
                    {link.label}
                    <span className="opacity-0 group-hover:opacity-100 transition-opacity">
                      →
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h4 className="text-slate-900 dark:text-white font-semibold mb-4 flex items-center gap-2">
              <Code className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
              Resources
            </h4>
            <ul className="space-y-3">
              {footerLinks.resources.map((link, index) => (
                <li key={index}>
                  {link.external ? (
                    <a
                      href={link.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-600 dark:text-slate-400 hover:text-cyan-600 dark:hover:text-cyan-400 text-sm transition-colors duration-200 flex items-center gap-1 group">
                      {link.label}
                      <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>
                  ) : (
                    <Link
                      to={link.to}
                      className="text-slate-600 dark:text-slate-400 hover:text-cyan-600 dark:hover:text-cyan-400 text-sm transition-colors duration-200 flex items-center gap-1 group">
                      {link.label}
                      <span className="opacity-0 group-hover:opacity-100 transition-opacity">
                        →
                      </span>
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Learn Links */}
          <div>
            <h4 className="text-slate-900 dark:text-white font-semibold mb-4 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              Learn
            </h4>
            <ul className="space-y-3">
              {footerLinks.learn.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.to}
                    className="text-slate-600 dark:text-slate-400 hover:text-purple-600 dark:hover:text-purple-400 text-sm transition-colors duration-200 flex items-center gap-1 group">
                    {link.label}
                    <span className="opacity-0 group-hover:opacity-100 transition-opacity">
                      →
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-slate-300 dark:border-slate-800/50 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-700 dark:text-slate-500 text-sm font-medium">
              Copyright © {currentYear} Physical AI & Humanoid Robotics. All rights reserved.
            </p>
            <div className="flex items-center gap-6 text-sm text-slate-700 dark:text-slate-500">
              <span className="flex items-center gap-2">
                Built with
                <span className="text-red-500 dark:text-red-400">❤️</span>
                using
              </span>
              <a
                href="https://docusaurus.io"
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                Docusaurus
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}


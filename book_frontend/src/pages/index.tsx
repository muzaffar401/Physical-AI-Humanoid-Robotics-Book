import React from 'react';
import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import { BookOpen, Code, Cpu, Zap, ArrowRight, Play } from 'lucide-react';

export default function Home(): ReactNode {
  return (
    <Layout
      title={`Home`}
      description="Master ROS 2, Gazebo simulation, autonomous navigation, and build voice-controlled AI-powered humanoid robots. A comprehensive course for developers and robotics enthusiasts.">
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950">
        {/* Hero Section */}
        <header className="relative overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
            <div className="absolute top-40 right-10 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse delay-700"></div>
            <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse delay-1000"></div>
          </div>

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24">
            {/* Main content */}
            <div className="text-center space-y-8 max-w-4xl mx-auto">
              {/* Badge */}
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-300 text-sm font-medium backdrop-blur-sm">
                <Zap className="w-4 h-4" />
                <span>From Basics to AI-Powered Robots</span>
              </div>

              {/* Title */}
              <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
                Master{' '}
                <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  ROS 2 & AI Robotics
                </span>
              </h1>

              {/* Subtitle */}
              <p className="text-xl md:text-2xl text-slate-300 leading-relaxed">
                Build Voice-Controlled Humanoid Robots with Advanced Navigation
              </p>

              {/* Description */}
              <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                A comprehensive course taking you from ROS 2 basics to building voice-controlled
                humanoid robots with AI perception and navigation. Perfect for software developers,
                AI engineers, and robotics enthusiasts.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
                <Link
                  to="/docs/intro"
                  className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/50 hover:scale-105 flex items-center gap-2 no-underline">
                  <Play className="w-5 h-5" />
                  Start Learning
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                
                <Link
                  to="/docs/module-1"
                  className="px-8 py-4 bg-white/5 backdrop-blur-sm border border-white/10 text-white rounded-xl font-semibold text-lg transition-all duration-300 hover:bg-white/10 hover:border-white/20 flex items-center gap-2 no-underline">
                  <BookOpen className="w-5 h-5" />
                  View Modules
                </Link>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto pt-12">
                {[
                  { number: '12+', label: 'Modules' },
                  { number: '50+', label: 'Projects' },
                  { number: '100%', label: 'Hands-On' }
                ].map((stat, i) => (
                  <div key={i} className="text-center">
                    <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                      {stat.number}
                    </div>
                    <div className="text-sm text-slate-400 mt-1">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </header>

        {/* Features Section */}
        <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-slate-900/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                What You'll Master
              </h2>
              <p className="text-slate-400 text-lg">
                Comprehensive curriculum designed for real-world robotics development
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: <Code className="w-8 h-8" />,
                  title: 'ROS 2 Fundamentals',
                  description: 'Master nodes, topics, services, and actions. Build a solid foundation in modern robotics middleware.',
                  color: 'from-blue-500 to-cyan-500'
                },
                {
                  icon: <Cpu className="w-8 h-8" />,
                  title: 'AI Integration',
                  description: 'Implement computer vision, voice control, and intelligent decision-making in your robots.',
                  color: 'from-purple-500 to-pink-500'
                },
                {
                  icon: <Zap className="w-8 h-8" />,
                  title: 'Autonomous Navigation',
                  description: 'Build robots that navigate complex environments using SLAM, path planning, and obstacle avoidance.',
                  color: 'from-cyan-500 to-blue-500'
                }
              ].map((feature, i) => (
                <div 
                  key={i} 
                  className="group relative bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl p-8 transition-all duration-300 hover:border-slate-700 hover:bg-slate-900/80 hover:transform hover:-translate-y-2"
                >
                  <div className={`inline-flex p-3 rounded-xl bg-gradient-to-r ${feature.color} mb-6 text-white`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400 leading-relaxed">
                    {feature.description}
                  </p>
                  <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                    <ArrowRight className="w-5 h-5 text-cyan-400" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-sm border border-blue-500/20 rounded-3xl p-12">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Ready to Build the Future?
              </h2>
              <p className="text-slate-300 text-lg mb-8">
                Join thousands of developers learning to create intelligent robots
              </p>
              <Link
                to="/docs/intro"
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl font-semibold text-lg transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/50 hover:scale-105 inline-flex items-center gap-2 no-underline">
                Get Started Now
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
}

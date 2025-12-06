import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  emoji: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'ROS 2 Fundamentals',
    emoji: '🤖',
    description: (
      <>
        Master the Robot Operating System 2 (ROS 2) with hands-on projects.
        Learn pub/sub communication, services, URDF robot descriptions, and visualization with RViz2.
      </>
    ),
  },
  {
    title: 'Simulation & Navigation',
    emoji: '🌍',
    description: (
      <>
        Build and simulate robots in Gazebo and NVIDIA Isaac Sim.
        Implement autonomous navigation with Nav2 stack, SLAM mapping, and path planning algorithms.
      </>
    ),
  },
  {
    title: 'AI-Powered Control',
    emoji: '🎙️',
    description: (
      <>
        Integrate voice commands, LLM-based planning, computer vision, and pose estimation.
        Create intelligent humanoid robots that understand and respond to natural language.
      </>
    ),
  },
  {
    title: 'Hands-On Projects',
    emoji: '⚙️',
    description: (
      <>
        Build real-world projects including sensor towers, autonomous delivery robots,
        and voice-controlled humanoids. Each module includes practical mini-projects.
      </>
    ),
  },
  {
    title: 'Industry-Ready Skills',
    emoji: '📚',
    description: (
      <>
        Learn the same tools and frameworks used by leading robotics companies.
        From Tesla to Boston Dynamics, ROS 2 powers the future of physical AI.
      </>
    ),
  },
  {
    title: 'Beginner Friendly',
    emoji: '🚀',
    description: (
      <>
        No prior robotics experience required! Start with Python basics and
        progress to advanced topics like VLAs and multi-modal AI integration.
      </>
    ),
  },
];

function Feature({title, emoji, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureEmoji}>{emoji}</div>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

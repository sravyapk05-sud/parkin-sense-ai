import 'package:flutter/material.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

class ParkinsonCarePage extends StatefulWidget {
  @override
  _ParkinsonCarePageState createState() => _ParkinsonCarePageState();
}

class _ParkinsonCarePageState extends State<ParkinsonCarePage> {
  late YoutubePlayerController _controller1;
  late YoutubePlayerController _controller2;
  bool _isLoading = true;
  int _selectedVideoIndex = 0;

  final List<VideoItem> _videos = [
    VideoItem(
      title: 'Understanding Parkinson\'s Disease',
      description: 'Basic overview of Parkinson\'s disease - Learn about symptoms, causes, and treatment options',
      url: 'https://www.youtube.com/watch?v=cRLB7WqX0fU',
      videoId: 'cRLB7WqX0fU',
    ),
    VideoItem(
      title: 'Screening Test For Parkinsons Disease',
      description: 'Learn about the screening methods and diagnostic tests for Parkinson\'s disease',
      url: 'https://www.youtube.com/watch?v=dgsaPeJh2Yg',
      videoId: 'dgsaPeJh2Yg',
    ),
  ];

  @override
  void initState() {
    super.initState();
    // _initializeYoutubePlayers();
  }

  void _initializeYoutubePlayers() {
    try {
      // Initialize first video controller
      _controller1 = YoutubePlayerController(
        initialVideoId: _videos[0].videoId,
        flags: YoutubePlayerFlags(
          autoPlay: false,
          mute: false,
          isLive: false,
          loop: false,
          disableDragSeek: false,
          enableCaption: true,
        ),
      );

      // Initialize second video controller
      _controller2 = YoutubePlayerController(
        initialVideoId: _videos[1].videoId,
        flags: YoutubePlayerFlags(
          autoPlay: false,
          mute: false,
          isLive: false,
          loop: false,
          disableDragSeek: false,
          enableCaption: true,
        ),
      );

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      print('Error initializing YouTube players: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _controller1.dispose();
    _controller2.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Parkinson\'s Care Guide',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: Colors.blue[800],
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.info_outline),
            onPressed: () {
              _showInfoDialog(context);
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

                     // Caregiver Instructions Section
            Container(
              color: Colors.blue[50],
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '📋 Important Instructions for Caregivers',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: Colors.blue[900],
                    ),
                  ),
                  SizedBox(height: 16),
                  _buildInstructionCard(
                    icon: Icons.medication,
                    title: 'Medication Management',
                    instructions: [
                      'Maintain a strict medication schedule',
                      'Use pill organizers to avoid missed doses',
                      'Keep a log of medication effects and side effects',
                      'Set alarms for medication times',
                      'Watch for "on-off" fluctuations',
                    ],
                  ),
                  _buildInstructionCard(
                    icon: Icons.fitness_center,
                    title: 'Exercise and Mobility',
                    instructions: [
                      'Encourage daily gentle exercises',
                      'Assist with stretching routines',
                      'Ensure safe walking paths at home',
                      'Consider physical therapy sessions',
                      'Practice balance exercises regularly',
                    ],
                  ),
                  _buildInstructionCard(
                    icon: Icons.restaurant,
                    title: 'Nutrition and Eating',
                    instructions: [
                      'Provide easy-to-eat, nutritious meals',
                      'Allow extra time for meals',
                      'Use adaptive utensils if needed',
                      'Ensure adequate hydration',
                      'Monitor weight changes',
                    ],
                  ),
                  _buildInstructionCard(
                    icon: Icons.health_and_safety,
                    title: 'Safety Precautions',
                    instructions: [
                      'Remove tripping hazards from floors',
                      'Install grab bars in bathrooms',
                      'Ensure good lighting throughout home',
                      'Keep emergency numbers accessible',
                      'Install handrails on staircases',
                    ],
                  ),
                  _buildInstructionCard(
                    icon: Icons.favorite,
                    title: 'Emotional Support',
                    instructions: [
                      'Be patient and understanding',
                      'Encourage social interactions',
                      'Listen actively to concerns',
                      'Consider support groups for both patient and caregiver',
                      'Watch for signs of depression',
                    ],
                  ),
                ],
              ),
            ),

            // Fall Prevention Tips
            Container(
              margin: EdgeInsets.all(16),
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [Colors.orange[50]!, Colors.orange[100]!],
                ),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.orange[200]!),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.warning_amber_rounded, color: Colors.orange[700], size: 28),
                      SizedBox(width: 8),
                      Text(
                        'Fall Prevention Checklist',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange[900],
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  ...['Install non-slip mats in bathroom',
                    'Keep pathways clear of clutter',
                    'Use night lights in hallways',
                    'Wear supportive, non-slip footwear',
                    'Remove loose rugs and carpets']
                      .map((tip) => Padding(
                    padding: EdgeInsets.only(bottom: 8),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.orange[700], size: 18),
                        SizedBox(width: 8),
                        Expanded(child: Text(tip)),
                      ],
                    ),
                  )),
                ],
              ),
            ),

            // Emergency Contact Section
            Container(
              margin: EdgeInsets.all(16),
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.red[50],
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.red[200]!),
              ),
              child: Column(
                children: [
                  Icon(
                    Icons.emergency,
                    color: Colors.red[700],
                    size: 40,
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Emergency Contacts',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.red[900],
                    ),
                  ),
                  SizedBox(height: 12),
                  _buildEmergencyContact(
                    'Neurologist',
                    'Dr. Sarah Johnson',
                    '(555) 123-4567',
                  ),
                  _buildEmergencyContact(
                    'Parkinson\'s Foundation',
                    '24/7 Helpline',
                    '1-800-4PD-INFO',
                  ),
                  _buildEmergencyContact(
                    'Emergency Services',
                    'Immediate Help',
                    '911',
                  ),
                  SizedBox(height: 16),
                  // ElevatedButton.icon(
                  //   onPressed: () {
                  //     // Add emergency call functionality
                  //   },
                  //   icon: Icon(Icons.phone),
                  //   label: Text('Call Emergency Services'),
                  //   style: ElevatedButton.styleFrom(
                  //     backgroundColor: Colors.red[700],
                  //     foregroundColor: Colors.white,
                  //     minimumSize: Size(double.infinity, 50),
                  //     shape: RoundedRectangleBorder(
                  //       borderRadius: BorderRadius.circular(10),
                  //     ),
                  //   ),
                  // ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _getVideoPlayer(int index) {
    return YoutubePlayer(
      controller: index == 0 ? _controller1 : _controller2,
      showVideoProgressIndicator: true,
      progressIndicatorColor: Colors.blue,
      progressColors: ProgressBarColors(
        playedColor: Colors.blue,
        handleColor: Colors.red,
        backgroundColor: Colors.grey,
        bufferedColor: Colors.lightBlue,
      ),
      controlsTimeOut: Duration(seconds: 3),
      bottomActions: [
        CurrentPosition(),
        ProgressBar(
          isExpanded: true,
          colors: ProgressBarColors(
            playedColor: Colors.blue,
            handleColor: Colors.blue,
          ),
        ),
        RemainingDuration(),
        FullScreenButton(),
      ],
    );
  }

  Widget _buildInstructionCard({
    required IconData icon,
    required String title,
    required List<String> instructions,
  }) {
    return Card(
      margin: EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Colors.blue[800], size: 24),
                SizedBox(width: 12),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.blue[900],
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            ...instructions.map((instruction) => Padding(
              padding: EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('• ', style: TextStyle(fontSize: 16, color: Colors.blue[700])),
                  Expanded(
                    child: Text(
                      instruction,
                      style: TextStyle(fontSize: 14, height: 1.3),
                    ),
                  ),
                ],
              ),
            )),
          ],
        ),
      ),
    );
  }

  Widget _buildEmergencyContact(String title, String name, String phone) {
    return Container(
      margin: EdgeInsets.only(bottom: 8),
      padding: EdgeInsets.symmetric(vertical: 8),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.red[100]!),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
              Text(
                name,
                style: TextStyle(
                  color: Colors.grey[600],
                  fontSize: 12,
                ),
              ),
            ],
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.red[700],
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              phone,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showInfoDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('About Parkinson\'s Care'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('This guide provides educational content about Parkinson\'s disease care.'),
              SizedBox(height: 12),
              Text('Features:'),
              SizedBox(height: 8),
              Text('• Educational videos about Parkinson\'s'),
              Text('• Caregiver instructions and tips'),
              Text('• Safety guidelines and precautions'),
              Text('• Emergency contact information'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Close'),
            ),
          ],
        );
      },
    );
  }
}

class VideoItem {
  final String title;
  final String description;
  final String url;
  final String videoId;

  VideoItem({
    required this.title,
    required this.description,
    required this.url,
    required this.videoId,
  });
}
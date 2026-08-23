// import 'dart:async';
// import 'dart:convert';
// import 'dart:io';
// import 'package:flutter/foundation.dart';
// import 'package:google_generative_ai/google_generative_ai.dart';
// import 'package:flutter/material.dart';
// import 'package:parkinsonsapp/homenew.dart';
// import 'package:shared_preferences/shared_preferences.dart';
// import 'package:image_picker/image_picker.dart';
// import 'package:file_picker/file_picker.dart';
//
// // Replace with your Gemini API key from: https://aistudio.google.com/app/apikeys
// const String GEMINI_API_KEY = 'AIzaSyAE1kwdALorgkTMhf5zdYjuePfnZAYPqCs';
//
// void main() {
//   runApp(const MyChatbotApp());
// }
//
// class MyChatbotApp extends StatelessWidget {
//   const MyChatbotApp({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Chatbot',
//       theme: ThemeData(
//         primarySwatch: Colors.blue,
//       ),
//       home: const MyChatPage(title: 'AI Chatbot Assistant'),
//     );
//   }
// }
//
// class MyChatPage extends StatefulWidget {
//   const MyChatPage({super.key, required this.title});
//
//   final String title;
//
//   @override
//   State<MyChatPage> createState() => _MyChatPageState();
// }
//
// class ChatMessage {
//   String messageContent;
//   String messageType;
//   String? imagePath;
//   String? imageBase64;
//
//   ChatMessage({
//     required this.messageContent,
//     required this.messageType,
//     this.imagePath,
//     this.imageBase64,
//   });
// }
//
// class _MyChatPageState extends State<MyChatPage> {
//   late GenerativeModel model;
//   late ChatSession chatSession;
//   String userName = "User";
//   String userUID = "";
//   bool _isDisposed = false;
//   bool _isLoading = false;
//   late SharedPreferences pref;
//
//   @override
//   void initState() {
//     super.initState();
//     _initializeChat();
//     _initializeAndLoadChat();
//   }
//
//   Future<void> _initializeAndLoadChat() async {
//     await _getUserName();
//     await _loadPreviousChat();
//   }
//
//   Future<void> _getUserName() async {
//     pref = await SharedPreferences.getInstance();
//     setState(() {
//       userName = pref.getString("uname") ?? "User";
//       userUID = pref.getString("lid") ?? "";
//     });
//   }
//
//   Future<void> _loadPreviousChat() async {
//     if (userUID.isEmpty) return;
//     final chatHistory = pref.getString('chat_history_$userUID');
//     if (chatHistory != null && chatHistory.isNotEmpty) {
//       try {
//         final List<dynamic> jsonList = jsonDecode(chatHistory);
//         setState(() {
//           messages = jsonList.map((json) {
//             return ChatMessage(
//               messageContent: json['content'] ?? '',
//               messageType: json['type'] ?? 'sender',
//               imageBase64: json['imageBase64'],
//               imagePath: json['imagePath'],
//             );
//           }).toList();
//         });
//         print("Loaded ${messages.length} previous messages");
//       } catch (e) {
//         print("Error decoding chat history: $e");
//       }
//     }
//   }
//
//   Future<void> _saveChatHistory() async {
//     if (messages.isEmpty || userUID.isEmpty) return;
//
//     final jsonList = messages.map((msg) => {
//       'type': msg.messageType,
//       'content': msg.messageContent,
//       'imageBase64': msg.imageBase64,
//       'imagePath': msg.imagePath,
//     }).toList();
//
//     final chatString = jsonEncode(jsonList);
//     await pref.setString('chat_history_$userUID', chatString);
//     // Also save to timestamped storage
//     await _saveCurrentChat();
//     print("Chat history saved");
//   }
//
//   Future<void> _saveCurrentChat() async {
//     if (messages.isEmpty || userUID.isEmpty) return;
//
//     final timestamp = DateTime.now().toString();
//     final jsonList = messages.map((msg) => {
//       'type': msg.messageType,
//       'content': msg.messageContent,
//       'imageBase64': msg.imageBase64,
//       'imagePath': msg.imagePath,
//     }).toList();
//
//     final chatString = jsonEncode(jsonList);
//     final allChats = pref.getStringList('all_chats_$userUID') ?? [];
//
//     // Store individual chat with timestamp
//     await pref.setString('chat_$userUID\_$timestamp', chatString);
//
//     // Add timestamp to list of all chats
//     if (!allChats.contains(timestamp)) {
//       allChats.insert(0, timestamp);
//       await pref.setStringList('all_chats_$userUID', allChats);
//     }
//
//     // Also store as current active chat
//     await pref.setString('chat_history_$userUID', chatString);
//     print('Chat saved with timestamp: $timestamp');
//   }
//
//   Future<List<String>> _getAllChatTimestamps() async {
//     if (userUID.isEmpty) return [];
//     return pref.getStringList('all_chats_$userUID') ?? [];
//   }
//
//   Future<void> _loadChatByTimestamp(String timestamp) async {
//     if (userUID.isEmpty) return;
//     final chatHistory = pref.getString('chat_$userUID\_$timestamp');
//     if (chatHistory != null && chatHistory.isNotEmpty) {
//       try {
//         final List<dynamic> jsonList = jsonDecode(chatHistory);
//         setState(() {
//           messages = jsonList.map((json) {
//             return ChatMessage(
//               messageContent: json['content'] ?? '',
//               messageType: json['type'] ?? 'sender',
//               imageBase64: json['imageBase64'],
//               imagePath: json['imagePath'],
//             );
//           }).toList();
//         });
//         print('Loaded chat from timestamp: $timestamp with ${messages.length} messages');
//       } catch (e) {
//         print("Error decoding timestamped chat: $e");
//       }
//     }
//   }
//
//   void _showPreviousChatsDialog() async {
//     // Check if user is logged in
//     if (userUID.isEmpty || userName == "User") {
//       ScaffoldMessenger.of(context).showSnackBar(
//         const SnackBar(content: Text('Please login to view chat history')),
//       );
//       return;
//     }
//
//     List<String> timestamps = await _getAllChatTimestamps();
//
//     if (timestamps.isEmpty) {
//       ScaffoldMessenger.of(context).showSnackBar(
//         const SnackBar(content: Text('No previous chats found')),
//       );
//       return;
//     }
//
//     showDialog(
//       context: context,
//       builder: (BuildContext context) {
//         return AlertDialog(
//           title: const Text('Previous Chats'),
//           content: SizedBox(
//             width: double.maxFinite,
//             child: ListView.builder(
//               itemCount: timestamps.length,
//               itemBuilder: (context, index) {
//                 final timestamp = timestamps[index];
//                 final dateTime = DateTime.parse(timestamp);
//                 final formattedDate = '${dateTime.day}/${dateTime.month}/${dateTime.year} ${dateTime.hour}:${dateTime.minute.toString().padLeft(2, '0')}';
//
//                 return ListTile(
//                   title: Text(formattedDate),
//                   leading: const Icon(Icons.chat_bubble_outline),
//                   onTap: () {
//                     _loadChatByTimestamp(timestamp);
//                     Navigator.pop(context);
//                     ScaffoldMessenger.of(context).showSnackBar(
//                       SnackBar(content: Text('Loaded chat from $formattedDate')),
//                     );
//                   },
//                 );
//               },
//             ),
//           ),
//           actions: [
//             TextButton(
//               onPressed: () => Navigator.pop(context),
//               child: const Text('Close'),
//             ),
//           ],
//         );
//       },
//     );
//   }
//
//   Future<void> _clearChatHistory() async {
//     if (userUID.isEmpty) return;
//     await pref.remove('chat_history_$userUID');
//     setState(() {
//       messages.clear();
//     });
//     ScaffoldMessenger.of(context).showSnackBar(
//       const SnackBar(content: Text('Chat history cleared')),
//     );
//     // Restart chat session
//     await _initializeChat();
//   }
//
//   Future<void> _pickAndSendImage() async {
//     try {
//       final ImagePicker picker = ImagePicker();
//       final XFile? image = await picker.pickImage(source: ImageSource.gallery);
//
//       if (image != null) {
//         final bytes = await image.readAsBytes();
//         final base64Image = base64Encode(bytes);
//
//         setState(() {
//           selectedImageBase64 = base64Image;
//           selectedImagePath = image.path;
//         });
//
//         ScaffoldMessenger.of(context).showSnackBar(
//           const SnackBar(content: Text('Image selected. Add text and send, or send directly.')),
//         );
//       }
//     } catch (e) {
//       print('Error picking image: $e');
//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text('Error picking image: $e')),
//       );
//     }
//   }
//
//   Future<void> _initializeChat() async {
//     // Initialize Gemini model
//     model = GenerativeModel(
//       model: 'gemini-2.5-flash-lite',
//       apiKey: GEMINI_API_KEY,
//     );
//
//     // Start a new chat session
//     chatSession = model.startChat();
//   }
//
//   List<ChatMessage> messages = [];
//   TextEditingController te_message = TextEditingController();
//   String? selectedImageBase64;
//   String? selectedImagePath;
//
//   Future<void> _sendMessage(String userMessage) async {
//     if ((userMessage.isEmpty && selectedImageBase64 == null) || _isLoading) return;
//
//     setState(() {
//       _isLoading = true;
//       messages.add(ChatMessage(
//         messageContent: userMessage.isEmpty ? 'Image shared' : userMessage,
//         messageType: "sender",
//         imageBase64: selectedImageBase64,
//         imagePath: selectedImagePath,
//       ));
//     });
//
//     te_message.clear();
//
//     try {
//       // Prepare the content to send
//       List<Part> parts = [];
//
//       // Add text if provided
//       if (userMessage.isNotEmpty) {
//         parts.add(TextPart(userMessage));
//       }
//
//       // Add image if selected
//       if (selectedImageBase64 != null && selectedImageBase64!.isNotEmpty) {
//         String mimeType = 'image/jpeg';
//         if (selectedImagePath != null) {
//           if (selectedImagePath!.toLowerCase().endsWith('.png')) {
//             mimeType = 'image/png';
//           } else if (selectedImagePath!.toLowerCase().endsWith('.gif')) {
//             mimeType = 'image/gif';
//           } else if (selectedImagePath!.toLowerCase().endsWith('.webp')) {
//             mimeType = 'image/webp';
//           }
//         }
//         parts.add(DataPart(mimeType, base64Decode(selectedImageBase64!)));
//       }
//
//       // Send message to Gemini
//       final Content content = parts.length > 1
//           ? Content.multi(parts)
//           : Content.text(userMessage);
//
//       final response = await chatSession.sendMessage(content);
//
//       // Add bot response to messages
//       if (response.text != null) {
//         setState(() {
//           messages.add(ChatMessage(
//             messageContent: response.text!,
//             messageType: "receiver",
//           ));
//         });
//       }
//
//       // Clear selected image after sending
//       setState(() {
//         selectedImageBase64 = null;
//         selectedImagePath = null;
//       });
//
//     } catch (e) {
//       // Show error message
//       setState(() {
//         messages.add(ChatMessage(
//           messageContent: 'Error: ${e.toString()}',
//           messageType: "receiver",
//         ));
//       });
//       print("Error sending message: $e");
//     } finally {
//       setState(() {
//         _isLoading = false;
//       });
//       // Save chat history after each message
//       await _saveChatHistory();
//     }
//   }
//
//   @override
//   void dispose() {
//     _isDisposed = true;
//     te_message.dispose();
//     super.dispose();
//   }
//
//   @override
//   void deactivate() {
//     super.deactivate();
//   }
//
//   @override
//   Widget build(BuildContext context) {
//     return WillPopScope(
//       onWillPop: () async {
//         Navigator.push(
//           context,
//           MaterialPageRoute(builder: (context) => home()),
//         );
//         return true;
//       },
//       child: Scaffold(
//         backgroundColor: Color.fromARGB(255, 228, 213, 231),
//         appBar: AppBar(
//           title: Text(
//             userName,
//             style: const TextStyle(color: Colors.white),
//           ),
//           leading: IconButton(
//             icon: const Icon(Icons.arrow_back),
//             onPressed: () {
//               _saveChatHistory();
//               Navigator.push(
//                 context,
//                 MaterialPageRoute(builder: (context) => HomeNew()),
//               );
//             },
//           ),
//           actions: [
//             PopupMenuButton(
//               onSelected: (value) {
//                 if (value == 'clear') {
//                   showDialog(
//                     context: context,
//                     builder: (BuildContext context) {
//                       return AlertDialog(
//                         title: const Text('Clear Chat History?'),
//                         content: const Text('Are you sure you want to clear all chat messages?'),
//                         actions: [
//                           TextButton(
//                             onPressed: () => Navigator.pop(context),
//                             child: const Text('Cancel'),
//                           ),
//                           TextButton(
//                             onPressed: () {
//                               _clearChatHistory();
//                               Navigator.pop(context);
//                             },
//                             child: const Text('Clear'),
//                           ),
//                         ],
//                       );
//                     },
//                   );
//                 } else if (value == 'new') {
//                   showDialog(
//                     context: context,
//                     builder: (BuildContext context) {
//                       return AlertDialog(
//                         title: const Text('Start New Chat?'),
//                         content: const Text('Current chat will be saved. Start a new conversation?'),
//                         actions: [
//                           TextButton(
//                             onPressed: () => Navigator.pop(context),
//                             child: const Text('Cancel'),
//                           ),
//                           TextButton(
//                             onPressed: () {
//                               setState(() {
//                                 messages.clear();
//                               });
//                               _initializeChat();
//                               Navigator.pop(context);
//                             },
//                             child: const Text('New Chat'),
//                           ),
//                         ],
//                       );
//                     },
//                   );
//                 } else if (value == 'view') {
//                   _showPreviousChatsDialog();
//                 }
//               },
//               itemBuilder: (BuildContext context) {
//                 List<PopupMenuEntry<String>> items = [];
//
//                 // Only show View History for logged-in users
//                 if (userUID.isNotEmpty && userName != "User") {
//                   items.add(
//                     const PopupMenuItem(
//                       value: 'view',
//                       child: Row(
//                         children: [
//                           Icon(Icons.history),
//                           SizedBox(width: 10),
//                           Text('View History'),
//                         ],
//                       ),
//                     ),
//                   );
//                 }
//
//                 items.addAll([
//                   const PopupMenuItem(
//                     value: 'new',
//                     child: Row(
//                       children: [
//                         Icon(Icons.add_circle_outline),
//                         SizedBox(width: 10),
//                         Text('New Chat'),
//                       ],
//                     ),
//                   ),
//                   const PopupMenuItem(
//                     value: 'clear',
//                     child: Row(
//                       children: [
//                         Icon(Icons.delete_outline),
//                         SizedBox(width: 10),
//                         Text('Clear History'),
//                       ],
//                     ),
//                   ),
//                 ]);
//
//                 return items;
//               },
//             ),
//           ],
//         ),
//         body: Stack(
//           children: <Widget>[
//             ListView.builder(
//               itemCount: messages.length,
//               shrinkWrap: true,
//               padding: const EdgeInsets.only(top: 10, bottom: 50),
//               physics: const ScrollPhysics(),
//               itemBuilder: (context, index) {
//                 return Container(
//                   padding: const EdgeInsets.only(
//                     left: 14,
//                     right: 14,
//                     top: 10,
//                     bottom: 10,
//                   ),
//                   child: Align(
//                     alignment: (messages[index].messageType == "receiver"
//                         ? Alignment.topLeft
//                         : Alignment.topRight),
//                     child: Container(
//                       decoration: BoxDecoration(
//                         borderRadius: BorderRadius.circular(20),
//                         color: (messages[index].messageType == "receiver"
//                             ? Colors.grey.shade200
//                             : Colors.blue[200]),
//                       ),
//                       padding: const EdgeInsets.all(16),
//                       child: Column(
//                         crossAxisAlignment: CrossAxisAlignment.start,
//                         children: [
//                           // Show image if present
//                           if (messages[index].imageBase64 != null && messages[index].imageBase64!.isNotEmpty)
//                             Padding(
//                               padding: const EdgeInsets.only(bottom: 8.0),
//                               child: ClipRRect(
//                                 borderRadius: BorderRadius.circular(12),
//                                 child: Image.memory(
//                                   base64Decode(messages[index].imageBase64!),
//                                   width: 200,
//                                   height: 200,
//                                   fit: BoxFit.cover,
//                                 ),
//                               ),
//                             ),
//                           // Show image path if present (for web preview)
//                           if (messages[index].imagePath != null && messages[index].imagePath!.isNotEmpty)
//                             if (!kIsWeb)
//                               Padding(
//                                 padding: const EdgeInsets.only(bottom: 8.0),
//                                 child: ClipRRect(
//                                   borderRadius: BorderRadius.circular(12),
//                                   child: Image.file(
//                                     File(messages[index].imagePath!),
//                                     width: 200,
//                                     height: 200,
//                                     fit: BoxFit.cover,
//                                   ),
//                                 ),
//                               ),
//                           // Show text message
//                           Text(
//                             messages[index].messageContent,
//                             style: const TextStyle(fontSize: 15),
//                           ),
//                         ],
//                       ),
//                     ),
//                   ),
//                 );
//               },
//             ),
//             // Loading indicator
//             if (_isLoading)
//               Align(
//                 alignment: Alignment.center,
//                 child: Container(
//                   padding: const EdgeInsets.all(8),
//                   decoration: BoxDecoration(
//                     color: Colors.grey.shade300,
//                     borderRadius: BorderRadius.circular(20),
//                   ),
//                   child: const SizedBox(
//                     width: 30,
//                     height: 30,
//                     child: CircularProgressIndicator(
//                       strokeWidth: 2,
//                     ),
//                   ),
//                 ),
//               ),
//             Align(
//               alignment: Alignment.bottomLeft,
//               child: Container(
//                 width: double.infinity,
//                 color: Colors.white,
//                 child: Column(
//                   mainAxisSize: MainAxisSize.min,
//                   children: [
//                     // Image preview if selected
//                     if (selectedImageBase64 != null && selectedImageBase64!.isNotEmpty)
//                       Padding(
//                         padding: const EdgeInsets.all(8.0),
//                         child: Stack(
//                           children: [
//                             ClipRRect(
//                               borderRadius: BorderRadius.circular(12),
//                               child: Image.memory(
//                                 base64Decode(selectedImageBase64!),
//                                 width: 100,
//                                 height: 100,
//                                 fit: BoxFit.cover,
//                               ),
//                             ),
//                             Positioned(
//                               right: 0,
//                               top: 0,
//                               child: GestureDetector(
//                                 onTap: () {
//                                   setState(() {
//                                     selectedImageBase64 = null;
//                                     selectedImagePath = null;
//                                   });
//                                 },
//                                 child: Container(
//                                   decoration: BoxDecoration(
//                                     color: Colors.red,
//                                     shape: BoxShape.circle,
//                                   ),
//                                   padding: const EdgeInsets.all(4),
//                                   child: const Icon(
//                                     Icons.close,
//                                     color: Colors.white,
//                                     size: 16,
//                                   ),
//                                 ),
//                               ),
//                             ),
//                           ],
//                         ),
//                       ),
//                     // Input row
//                     Container(
//                       padding: const EdgeInsets.only(
//                         left: 10,
//                         bottom: 10,
//                         top: 10,
//                       ),
//                       height: 60,
//                       width: double.infinity,
//                       color: Colors.white,
//                       child: Row(
//                         children: <Widget>[
//                           // Add button
//                           GestureDetector(
//                             onTap: () {},
//                             child: Container(
//                               height: 30,
//                               width: 30,
//                               decoration: BoxDecoration(
//                                 color: Colors.cyan,
//                                 borderRadius: BorderRadius.circular(30),
//                               ),
//                               child: const Icon(
//                                 Icons.add,
//                                 color: Colors.white,
//                                 size: 20,
//                               ),
//                             ),
//                           ),
//                           const SizedBox(width: 10),
//                           // Image picker button
//                           GestureDetector(
//                             onTap: () {
//                               _pickAndSendImage();
//                             },
//                             child: Container(
//                               height: 30,
//                               width: 30,
//                               decoration: BoxDecoration(
//                                 color: selectedImageBase64 != null && selectedImageBase64!.isNotEmpty
//                                     ? Colors.orange
//                                     : Colors.green,
//                                 borderRadius: BorderRadius.circular(30),
//                               ),
//                               child: const Icon(
//                                 Icons.image,
//                                 color: Colors.white,
//                                 size: 20,
//                               ),
//                             ),
//                           ),
//                           const SizedBox(width: 15),
//                           Expanded(
//                             child: TextField(
//                               controller: te_message,
//                               decoration: const InputDecoration(
//                                 hintText: "Write message...",
//                                 hintStyle: TextStyle(color: Colors.black54),
//                                 border: InputBorder.none,
//                               ),
//                               onSubmitted: (value) {
//                                 if (value.isNotEmpty || selectedImageBase64 != null) {
//                                   _sendMessage(value);
//                                 }
//                               },
//                             ),
//                           ),
//                           const SizedBox(width: 15),
//                           FloatingActionButton(
//                             onPressed: () async {
//                               String message = te_message.text.trim();
//                               if ((message.isNotEmpty || selectedImageBase64 != null) && !_isLoading) {
//                                 await _sendMessage(message);
//                               }
//                             },
//                             backgroundColor: Colors.cyan,
//                             elevation: 0,
//                             child: const Icon(
//                               Icons.send,
//                               color: Colors.white,
//                               size: 18,
//                             ),
//                           ),
//                         ],
//                       ),
//                     ),
//                   ],
//                 ),
//               ),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ChatBotPage extends StatefulWidget {
  const ChatBotPage({super.key});

  @override
  State<ChatBotPage> createState() => _ChatBotPageState();
}

class _ChatBotPageState extends State<ChatBotPage> {
  late GenerativeModel _model;
  late ChatSession _session;
  final List<Map<String, String>> _messages = [];
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _initializeModel();
  }

  Future<void> _initializeModel() async {
    try {
      // Get API key from SharedPreferences (safer than hardcoding)
      final prefs = await SharedPreferences.getInstance();
      final apiKey = "AIzaSyD6WmfsBs3kWh3DcHs8GQtTcc4kSX-gwLM";

      // Initialize the model - use appropriate model for your needs
      _model = GenerativeModel(
        model: 'gemini-2.5-flash-lite', // or 'gemini-pro', 'gemini-1.5-pro'
        apiKey: apiKey,
        generationConfig: GenerationConfig(
          temperature: 0.7,
          maxOutputTokens: 1024,
        ),
      );

      _session = _model.startChat();

      setState(() {
        _errorMessage = null;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to initialize chatbot: $e';
      });
    }
  }

  Future<void> _sendMessage(String message) async {
    if (message.trim().isEmpty || _isLoading) return;

    setState(() {
      _messages.add({'role': 'user', 'content': message});
      _isLoading = true;
      _errorMessage = null;
    });

    _scrollToBottom();

    try {
      // Send message to Gemini
      final response = await _session.sendMessage(
        Content.text(message),
      );

      setState(() {
        _messages.add({
          'role': 'model',
          'content': response.text ?? 'No response received'
        });
        _isLoading = false;
      });

      _scrollToBottom();
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: $e';
        _isLoading = false;
      });
    }

    _controller.clear();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _clearChat() {
    setState(() {
      _messages.clear();
      _session = _model.startChat(); // Start fresh session
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI ChatBot'),
        backgroundColor: Colors.blue[800],
        elevation: 4,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _clearChat,
            tooltip: 'Clear chat',
          ),
        ],
      ),
      body: Column(
        children: [
          // Error message if any
          if (_errorMessage != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(8),
              color: Colors.red[100],
              child: Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red),
                textAlign: TextAlign.center,
              ),
            ),

          // Chat messages
          Expanded(
            child: _messages.isEmpty
                ? _buildEmptyState()
                : ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message['role'] == 'user';

                return _buildMessageBubble(
                  message['content']!,
                  isUser,
                );
              },
            ),
          ),

          // Loading indicator
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),

          // Input area
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.chat_bubble_outline,
            size: 80,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          Text(
            'Start a conversation',
            style: TextStyle(
              fontSize: 20,
              color: Colors.grey[600],
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Ask me anything!',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey[500],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(String content, bool isUser) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!isUser) ...[
            CircleAvatar(
              radius: 16,
              backgroundColor: Colors.blue[800],
              child: const Icon(Icons.android, size: 18, color: Colors.white),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isUser ? Colors.blue[800] : Colors.grey[200],
                borderRadius: BorderRadius.circular(16).copyWith(
                  bottomLeft: isUser ? const Radius.circular(16) : const Radius.circular(4),
                  bottomRight: isUser ? const Radius.circular(4) : const Radius.circular(16),
                ),
              ),
              child: Text(
                content,
                style: TextStyle(
                  color: isUser ? Colors.white : Colors.black87,
                  fontSize: 16,
                ),
              ),
            ),
          ),
          if (isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              radius: 16,
              backgroundColor: Colors.green[700],
              child: const Icon(Icons.person, size: 18, color: Colors.white),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            offset: const Offset(0, -2),
            blurRadius: 4,
            color: Colors.grey.withOpacity(0.2),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'Type your message...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
              maxLines: null,
              textInputAction: TextInputAction.send,
              onSubmitted: _sendMessage,
            ),
          ),
          const SizedBox(width: 8),
          FloatingActionButton(
            onPressed: _isLoading ? null : () => _sendMessage(_controller.text),
            mini: true,
            backgroundColor: Colors.blue[800],
            child: _isLoading
                ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            )
                : const Icon(Icons.send, color: Colors.white),
          ),
        ],
      ),
    );
  }
}
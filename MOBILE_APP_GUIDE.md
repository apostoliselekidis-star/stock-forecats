# 📱 Mobile App Implementation Guide

## Option 1: Flutter (RECOMMENDED)

### Why Flutter?
- Native iOS + Android from one codebase
- Excellent performance
- Google-backed
- 60+ FPS animations
- Hot reload development

---

## Flutter Project Structure

```
stock_forecats_mobile/
├── lib/
│   ├── main.dart                 ← Entry point
│   ├── screens/
│   │   ├── home_screen.dart      ← Main analysis page
│   │   ├── screener_screen.dart  ← Stock screener
│   │   └── portfolio_screen.dart ← Portfolio tracking
│   ├── models/
│   │   ├── stock_model.dart      ← Data classes
│   │   ├── score_model.dart      ← Scoring response
│   │   └── recommendation.dart
│   ├── services/
│   │   └── api_service.dart      ← Backend API calls
│   └── widgets/
│       ├── recommendation_card.dart
│       ├── score_indicator.dart
│       └── chart_widget.dart
├── pubspec.yaml                  ← Dependencies
└── README.md
```

---

## Flutter Code Skeleton

### 1. pubspec.yaml (Dependencies)

```yaml
name: stock_forecats
description: Stock Analyzer Mobile App

version: 1.0.0+1

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  
  # API & Data
  http: ^1.1.0
  dio: ^5.3.0
  json_serializable: ^6.7.0
  
  # Charts
  fl_chart: ^0.64.0
  syncfusion_flutter_charts: ^22.2.0
  
  # State Management
  riverpod: ^2.4.0
  riverpod_generator: ^2.3.0
  
  # UI
  google_fonts: ^5.1.0
  flutter_svg: ^2.0.0
  badges: ^3.1.0
  
  # Storage
  hive: ^2.2.0
  hive_flutter: ^1.1.0
  
  # Other
  intl: ^0.19.0
  cached_network_image: ^3.3.0
  url_launcher: ^6.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.0
  riverpod_generator: ^2.3.0
  json_serializable: ^6.7.0
```

### 2. main.dart (Entry Point)

```dart
import 'package:flutter/material.dart';
import 'package:riverpod/riverpod.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stock Forecats',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        brightness: Brightness.light,
      ),
      darkTheme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        brightness: Brightness.dark,
      ),
      themeMode: ThemeMode.system,
      home: const HomeScreen(),
    );
  }
}
```

### 3. models/score_model.dart

```dart
import 'package:json_annotation/json_annotation.dart';

part 'score_model.g.dart';  // Generated file

@JsonSerializable()
class ScoreResponse {
  final String ticker;
  final double currentPrice;
  final Summary summary;
  final TechnicalScore technical;
  final FundamentalScore fundamental;
  final ForecastScore forecast;
  final SentimentScore sentiment;

  ScoreResponse({
    required this.ticker,
    required this.currentPrice,
    required this.summary,
    required this.technical,
    required this.fundamental,
    required this.forecast,
    required this.sentiment,
  });

  factory ScoreResponse.fromJson(Map<String, dynamic> json) =>
      _$ScoreResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ScoreResponseToJson(this);
}

@JsonSerializable()
class Summary {
  final double score;
  final String recommendation;
  final String emoji;
  final String description;
  final String riskLevel;
  final String confidence;

  Summary({
    required this.score,
    required this.recommendation,
    required this.emoji,
    required this.description,
    required this.riskLevel,
    required this.confidence,
  });

  factory Summary.fromJson(Map<String, dynamic> json) =>
      _$SummaryFromJson(json);
  Map<String, dynamic> toJson() => _$SummaryToJson(this);
}

@JsonSerializable()
class TechnicalScore {
  final double score;
  final String reasoning;
  
  TechnicalScore({
    required this.score,
    required this.reasoning,
  });

  factory TechnicalScore.fromJson(Map<String, dynamic> json) =>
      _$TechnicalScoreFromJson(json);
  Map<String, dynamic> toJson() => _$TechnicalScoreToJson(this);
}

@JsonSerializable()
class FundamentalScore {
  final double score;
  final String reasoning;
  
  FundamentalScore({
    required this.score,
    required this.reasoning,
  });

  factory FundamentalScore.fromJson(Map<String, dynamic> json) =>
      _$FundamentalScoreFromJson(json);
  Map<String, dynamic> toJson() => _$FundamentalScoreToJson(this);
}

@JsonSerializable()
class ForecastScore {
  final double score;
  final String reasoning;
  final String confidence;
  
  ForecastScore({
    required this.score,
    required this.reasoning,
    required this.confidence,
  });

  factory ForecastScore.fromJson(Map<String, dynamic> json) =>
      _$ForecastScoreFromJson(json);
  Map<String, dynamic> toJson() => _$ForecastScoreToJson(this);
}

@JsonSerializable()
class SentimentScore {
  final double score;
  final String reasoning;
  final String sentiment;
  
  SentimentScore({
    required this.score,
    required this.reasoning,
    required this.sentiment,
  });

  factory SentimentScore.fromJson(Map<String, dynamic> json) =>
      _$SentimentScoreFromJson(json);
  Map<String, dynamic> toJson() => _$SentimentScoreToJson(this);
}
```

### 4. services/api_service.dart

```dart
import 'package:dio/dio.dart';
import '../models/score_model.dart';

class ApiService {
  static const String baseUrl = 'https://stock-forecats-USERNAME.streamlit.app/api';
  
  late Dio _dio;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ));
  }

  /// Get complete stock score and recommendation
  Future<ScoreResponse> getStockScore({
    required String ticker,
    String period = '1y',
    int forecastDays = 7,
  }) async {
    try {
      final response = await _dio.get(
        '/score',
        queryParameters: {
          'ticker': ticker,
          'period': period,
          'forecast_days': forecastDays,
        },
      );
      
      return ScoreResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Get chart data for a stock
  Future<List<ChartPoint>> getChartData({
    required String ticker,
    String period = '1y',
  }) async {
    try {
      final response = await _dio.get(
        '/chart',
        queryParameters: {
          'ticker': ticker,
          'period': period,
        },
      );
      
      return (response.data as List)
          .map((e) => ChartPoint.fromJson(e))
          .toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  /// Screen stocks by sector
  Future<List<ScreenerResult>> screenStocks({
    required String sector,
    int limit = 10,
    double minScore = 5.5,
  }) async {
    try {
      final response = await _dio.get(
        '/screen',
        queryParameters: {
          'sector': sector,
          'limit': limit,
          'min_score': minScore,
        },
      );
      
      return (response.data as List)
          .map((e) => ScreenerResult.fromJson(e))
          .toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException error) {
    if (error.type == DioExceptionType.connectionTimeout) {
      return 'Connection timeout. Check your internet.';
    } else if (error.type == DioExceptionType.receiveTimeout) {
      return 'Server took too long to respond.';
    } else if (error.response?.statusCode == 404) {
      return 'Stock not found.';
    } else if (error.response?.statusCode == 500) {
      return 'Server error. Try again later.';
    } else {
      return 'Error: ${error.message}';
    }
  }
}
```

### 5. screens/home_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:riverpod/riverpod.dart';
import '../services/api_service.dart';
import '../models/score_model.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final TextEditingController _tickerController = TextEditingController();
  String? _selectedTicker;

  @override
  void initState() {
    super.initState();
    _tickerController.text = 'AAPL';
    _selectedTicker = 'AAPL';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Stock Forecats'),
        centerTitle: true,
        elevation: 0,
      ),
      body: Column(
        children: [
          // Search Bar
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _tickerController,
              textCapitalization: TextCapitalization.characters,
              onChanged: (value) {
                setState(() => _selectedTicker = value.toUpperCase());
              },
              decoration: InputDecoration(
                hintText: 'Enter ticker (e.g., AAPL)',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                suffixIcon: _tickerController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _tickerController.clear();
                          setState(() => _selectedTicker = null);
                        },
                      )
                    : null,
              ),
            ),
          ),
          
          // Results
          if (_selectedTicker != null && _selectedTicker!.isNotEmpty)
            Expanded(
              child: _buildStockAnalysis(_selectedTicker!),
            )
          else
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.search, size: 64, color: Colors.grey),
                    SizedBox(height: 16),
                    Text('Enter a stock ticker to analyze'),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildStockAnalysis(String ticker) {
    return FutureBuilder<ScoreResponse>(
      future: ApiService().getStockScore(ticker: ticker),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }

        if (snapshot.hasError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error, size: 64, color: Colors.red),
                const SizedBox(height: 16),
                Text('Error: ${snapshot.error}'),
              ],
            ),
          );
        }

        final data = snapshot.data!;
        final summary = data.summary;

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Recommendation Card
              _buildRecommendationCard(summary),
              const SizedBox(height: 16),

              // Score Breakdown
              _buildScoreCard(
                title: 'Technical Analysis',
                score: data.technical.score,
                reasoning: data.technical.reasoning,
              ),
              const SizedBox(height: 12),

              _buildScoreCard(
                title: 'Fundamentals',
                score: data.fundamental.score,
                reasoning: data.fundamental.reasoning,
              ),
              const SizedBox(height: 12),

              _buildScoreCard(
                title: 'Forecast',
                score: data.forecast.score,
                reasoning: data.forecast.reasoning,
              ),
              const SizedBox(height: 12),

              _buildScoreCard(
                title: 'Sentiment',
                score: data.sentiment.score,
                reasoning: data.sentiment.reasoning,
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildRecommendationCard(Summary summary) {
    final bgColor = _getRecommendationColor(summary.recommendation);
    
    return Card(
      elevation: 4,
      color: bgColor,
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Text(
              summary.emoji,
              style: const TextStyle(fontSize: 48),
            ),
            const SizedBox(height: 8),
            Text(
              summary.recommendation,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              summary.description,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 14),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildInfoBadge('Score', '${summary.score.toStringAsFixed(1)}/10'),
                _buildInfoBadge('Risk', summary.riskLevel),
                _buildInfoBadge('Confidence', summary.confidence),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildScoreCard({
    required String title,
    required double score,
    required String reasoning,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Chip(label: Text('${score.toStringAsFixed(1)}/10')),
              ],
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(
              value: score / 10,
              minHeight: 8,
              borderRadius: BorderRadius.circular(4),
            ),
            const SizedBox(height: 8),
            Text(
              reasoning,
              style: const TextStyle(fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoBadge(String label, String value) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 12, color: Colors.grey),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Color _getRecommendationColor(String recommendation) {
    switch (recommendation) {
      case 'STRONG BUY':
        return Colors.green.shade200;
      case 'BUY':
        return Colors.lightGreen.shade200;
      case 'HOLD':
        return Colors.yellow.shade200;
      case 'SELL':
        return Colors.red.shade200;
      case 'STRONG SELL':
        return Colors.red.shade300;
      default:
        return Colors.grey.shade200;
    }
  }
}

class ChartPoint {
  final DateTime date;
  final double close;

  ChartPoint({required this.date, required this.close});

  factory ChartPoint.fromJson(Map<String, dynamic> json) {
    return ChartPoint(
      date: DateTime.parse(json['date']),
      close: json['close'].toDouble(),
    );
  }
}

class ScreenerResult {
  final String ticker;
  final String company;
  final double score;
  final String recommendation;
  final double upside;

  ScreenerResult({
    required this.ticker,
    required this.company,
    required this.score,
    required this.recommendation,
    required this.upside,
  });

  factory ScreenerResult.fromJson(Map<String, dynamic> json) {
    return ScreenerResult(
      ticker: json['ticker'],
      company: json['company'],
      score: json['score'].toDouble(),
      recommendation: json['recommendation'],
      upside: json['upside'].toDouble(),
    );
  }
}
```

---

## To Create Flutter Project:

```bash
# Install Flutter (flutter.dev/docs/get-started)

# Create project
flutter create stock_forecats_mobile

# Add dependencies
cd stock_forecats_mobile
flutter pub add http riverpod fl_chart google_fonts

# Run
flutter run
```

---

## MY RECOMMENDATION

**Timeline**:
1. **This week**: Deploy web to Streamlit Cloud (5 min)
2. **Next month**: Build Flutter app alongside (2-4 weeks)
3. **Month 3**: Launch both web + mobile

**Cost**: FREE (web) + $125 (mobile app stores)

Ready to deploy the web app first? 🚀

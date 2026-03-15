// src/app/index.tsx
import React from "react";
import { AppNavigator } from "../navigation/AppNavigator";
import { ThemedView } from "../components/themed-view";
import { SafeAreaView } from "react-native-safe-area-context";
import { StyleSheet } from "react-native";
import { BottomTabInset, Spacing, MaxContentWidth } from "../constants/theme";

export default function Index() {
  return (
    <ThemedView style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <AppNavigator />
      </SafeAreaView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeArea: {
    flex: 1,
    paddingHorizontal: Spacing.four,
    paddingBottom: BottomTabInset + Spacing.three,
    maxWidth: MaxContentWidth,
  },
});

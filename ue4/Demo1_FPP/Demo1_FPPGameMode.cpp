// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "Demo1_FPPGameMode.h"
#include "Demo1_FPPHUD.h"
#include "Demo1_FPPCharacter.h"
#include "UObject/ConstructorHelpers.h"

ADemo1_FPPGameMode::ADemo1_FPPGameMode()
	: Super()
{
	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnClassFinder(TEXT("/Game/FirstPersonCPP/Blueprints/FirstPersonCharacter"));
	DefaultPawnClass = PlayerPawnClassFinder.Class;

	// use our custom HUD class
	HUDClass = ADemo1_FPPHUD::StaticClass();
}

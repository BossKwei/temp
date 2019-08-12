// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#pragma once 

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "Demo1_FPPHUD.generated.h"

UCLASS()
class ADemo1_FPPHUD : public AHUD
{
	GENERATED_BODY()

public:
	ADemo1_FPPHUD();

	/** Primary draw call for the HUD */
	virtual void DrawHUD() override;

private:
	/** Crosshair asset pointer */
	class UTexture2D* CrosshairTex;

};

